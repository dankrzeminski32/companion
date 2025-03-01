"""Core HTTP Server module"""

import socket
import select
import queue
from collections import defaultdict
import logging
from companion.handler import HttpRequestHandler
from companion.parser import HttpParser
from pathlib import Path
import argparse

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
argparser = argparse.ArgumentParser()

argparser.add_argument(
    "staticdir",
    help="folder from which content will be served by the web server",
    type=str,
)
argparser.add_argument(
    "--port", help="port for the web server socket to listen on", type=int
)


HOST = "localhost"
DEFAULT_PORT = 8180
CHUNK_SIZE = 1024
END_HTTP_REQUEST = "\r\n\r\n"


class HttpServer:
    """HTTP 1.0 server, supports GET and HEAD methods

    Uses Select and non-blocking sockets to handle multiple connections

    Attributes:
        inputs (list[socket.socket]): set of input fds for select call
        outputs (list[socket.socket]): set of output fds for select call
        exceptions (list[socket.socket]): set of exception fds for select call
        out_messages (dict[socket.socket, queue.Queue]): map of socket to it's ready-to-send messages
        in_messages (dict[socket.socket, bytes]): map of socket to it's read bytes

    Args:
        staticdir (Path): path to static assets (e.g. HTML, PNG)
        port (int): port number to serve the application
        host (str): host to serve the application on
    """

    inputs: list[socket.socket] = []
    outputs: list[socket.socket] = []
    exceptions: list[socket.socket] = []
    out_messages: dict[socket.socket, queue.Queue] = defaultdict(queue.Queue)
    in_messages: dict[socket.socket, bytes] = defaultdict(bytes)

    def __init__(self, staticdir: Path, port: int, host: str):
        logger.info(f"Setting static content directory {staticdir}")
        self.staticdir = staticdir
        self.request_handler = HttpRequestHandler(file_directory=self.staticdir)
        self.port = port
        self.host = host
        logger.info("Creating Server socket")
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setblocking(0)
        self.server_sock.bind((host, port))
        self.server_sock.listen(5)

    def run(self) -> None:
        """Runs the server's event loop, serving all connections"""
        self.inputs.append(self.server_sock)
        try:
            while True:
                read_list, write_list, exception_list = select.select(
                    self.inputs, self.outputs, self.exceptions
                )
                for conn in read_list:
                    if conn == self.server_sock:
                        new_connection, address = conn.accept()
                        new_connection.setblocking(0)
                        self.inputs.append(new_connection)
                        break
                    is_ready_for_send = self.handle_read(conn)
                    if is_ready_for_send:
                        self.inputs.remove(conn)
                        self.outputs.append(conn)
                    elif conn not in self.inputs:
                        self.inputs.remove(conn)
                for conn in write_list:
                    self.handle_write(conn)
                    self.outputs.remove(conn)
                    conn.close()
                for conn in exception_list:
                    self.handle_exception(conn)
        except Exception as exc:
            logger.exception(exc)
            self.server_sock.close()

    def handle_read(self, connection: socket.socket) -> bool:
        """Reads bytes off the network buffer

        Attempts to make a valid HTTP Request object

        If an object can't be created, it stores the current bytes and moves on

        Args:
            connection (socket.socket): socket to read from

        Returns:
            bool: True if the request is processed successfully, False if an error is encountered
        """
        logger.info(f"Handling read connection {connection}.")
        try:
            http_request_bytes = self.read_http_request(connection)
        except OSError:
            return False
        if http_request_bytes:
            http_request = HttpParser(http_request_bytes).parse()
            logger.info(f"Incoming Request {http_request}")
            http_response = self.request_handler.handle(http_request)
            self.out_messages[connection].put_nowait(http_response.bytes)
            return True
        else:
            connection.close()
            self.inputs.remove(connection)
            self.outputs.remove(connection)
            return False

    def handle_write(self, connection: socket.socket) -> None:
        """Writes an HttpResponse to the network buffer

        Args:
            connection (socket.socket): socket to write to
        """
        logger.info(f"Handling write connection {connection}.")
        message = self.out_messages[connection].get_nowait()
        logger.info(f"Sending Response {message}")
        connection.sendall(message)
        connection.close()

    def handle_exception(self, connection: socket.socket) -> None:
        """Closes HTTP connection when a socket encounters an exception.

        This could be improved to handle specific use cases.

        Args:
            connection (socket.socket): socket where the exception is occurring
        """
        logger.info(f"Handling exception connection {connection}, closing socket.")
        connection.close()

    def read_http_request(self, connection: socket.socket) -> bytes:
        """Attempts to identify bytes for an HTTP request from data in our internal buffer and date being read from the network buffer

        Args:
            connection (socket.socket): socket to read from

        Returns:
            bytes: bytes of a potential HTTP request
        """
        data = b""
        while True:
            data = connection.recv(CHUNK_SIZE)
            if not data:
                return False
            self.in_messages[connection] += data
            if data.decode("ascii")[-4:] == END_HTTP_REQUEST:
                http_bytes = self.in_messages[connection]
                del self.in_messages[connection]
                return http_bytes


def cli() -> None:
    """Target function to run from the CLI"""
    args = argparser.parse_args()
    static_content_dir = Path(args.staticdir).resolve()
    port = args.port if args.port else DEFAULT_PORT
    logger.info(f"Attempting to listen on port {port}")
    HttpServer(static_content_dir, port, HOST).run()
