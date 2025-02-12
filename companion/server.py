import socket
import select
import queue
from collections import defaultdict
import logging
from companion.handler import HttpRequestHandler
from companion.parser import HttpParser
from pathlib import Path

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


HOST = "localhost"
PORT = 8181
CHUNK_SIZE = 1024
END_HTTP_REQUEST = "\r\n\r\n"

STATIC_FILE_DIR = Path("C:/Users/dankr/OneDrive/Desktop/companion/testfolder")

inputs = []
outputs = []
exceptions = []

messages = defaultdict(queue.Queue)
request_handler = HttpRequestHandler(file_directory=STATIC_FILE_DIR)


def read_http_request(connection):
    found_end = False
    data = b""
    while not found_end:
        data += connection.recv(CHUNK_SIZE)
        if not data:
            break
        if data.decode("ascii")[-4:] == END_HTTP_REQUEST:
            found_end = True
    return data


def handle_read(connection):
    http_request_bytes = read_http_request(connection)
    http_request = HttpParser(http_request_bytes).parse()
    logger.info(f"Incoming Request {http_request}")
    http_response = request_handler.handle(http_request)
    messages[connection].put_nowait(http_response.bytes)


def handle_write(connection: socket.socket):
    message = messages[connection].get_nowait()
    logger.info(f"Sending Response {message}")
    connection.sendall(message)
    

def handle_exception(connection):
    logger.info("Handling exception connection")
    ...


def initialize_server_socket() -> socket.socket:
    logger.info("Creating Server socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind((HOST, PORT))
    sock.listen(5)
    return sock


def run_forever():
    server_socket = initialize_server_socket()
    inputs.append(server_socket)
    try:
        while True:
            read_list, write_list, exception_list = select.select(inputs, outputs, exceptions)
            for conn in read_list:
                if conn == server_socket:
                    new_connection, address = conn.accept()
                    new_connection.setblocking(0)
                    inputs.append(new_connection)
                    break
                handle_read(conn)
                inputs.remove(conn)
                outputs.append(conn)
            for conn in write_list:
                handle_write(conn)
                outputs.remove(conn)
                conn.close()
            for conn in exception_list:
                handle_exception(conn)
    except Exception as exc:
        logger.exception(exc)
        server_socket.close()


def cli():
    run_forever()