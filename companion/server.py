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

argparser.add_argument("staticdir", help="folder from which content will be served by the web server", type=str)
argparser.add_argument("--port", help="port for the web server socket to listen on", type=int)


HOST = "localhost"
DEFAULT_PORT = 8180
CHUNK_SIZE = 1024
END_HTTP_REQUEST = "\r\n\r\n"


class HttpServer:
    inputs = []
    outputs = []
    exceptions = []
    messages = defaultdict(queue.Queue)

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
    
    def run(self):
        self.inputs.append(self.server_sock)
        try:
            while True:
                read_list, write_list, exception_list = select.select(self.inputs, self.outputs, self.exceptions)
                for conn in read_list:
                    if conn == self.server_sock:
                        new_connection, address = conn.accept()
                        new_connection.setblocking(0)
                        self.inputs.append(new_connection)
                        break
                    is_ready_for_send = self.handle_read(conn)
                    self.inputs.remove(conn)
                    if is_ready_for_send:
                        self.outputs.append(conn)
                for conn in write_list:
                    self.handle_write(conn)
                    self.outputs.remove(conn)
                    conn.close()
                for conn in exception_list:
                    self.handle_exception(conn)
        except Exception as exc:
            logger.exception(exc)
            self.server_sock.close()

    def handle_read(self, connection):
        http_request_bytes = self.read_http_request(connection)
        if http_request_bytes:
            http_request = HttpParser(http_request_bytes).parse()
            logger.info(f"Incoming Request {http_request}")
            http_response = self.request_handler.handle(http_request)
            self.messages[connection].put_nowait(http_response.bytes)
            return True
        else:
            connection.close()
            return False

    def handle_write(self, connection: socket.socket):
        message = self.messages[connection].get_nowait()
        logger.info(f"Sending Response {message}")
        connection.sendall(message)
        connection.close()

    def handle_exception(self, connection):
        logger.info("Handling exception connection")
        ...
        
    def read_http_request(self, connection):
        found_end = False
        data = b""
        while not found_end:
            data += connection.recv(CHUNK_SIZE)
            if not data:
                return None
            if data.decode("ascii")[-4:] == END_HTTP_REQUEST:
                found_end = True
        return data


def cli():
    args = argparser.parse_args()
    static_content_dir = Path(args.staticdir).resolve()
    port = args.port if args.port else DEFAULT_PORT
    logger.info(f"Attempting to listen on port {port}")
    HttpServer(static_content_dir, port, HOST).run()
