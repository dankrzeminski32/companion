from companion.parser import HttpParser
import socket

HOST = "localhost"
PORT = 8181
CHUNK_SIZE = 10
END_HTTP_REQUEST = "\r\n\r\n"


def read_http_request(socket):
    found_end = False
    data = b""
    while not found_end:
        data += socket.recv(1024)
        if not data:
            break
        if data.decode("utf-8")[-4:] == END_HTTP_REQUEST:
            found_end = True
    return data


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))

sock.listen(1)


def run_forever():
    try:
        while True:
            conn, address = sock.accept()
            while True:
                http_data = read_http_request(conn)
                if not http_data:
                    break
                http_request = HttpParser(http_data).parse()
                conn.sendall(b"thanks for chatting")
                print(str(http_request))
            conn.close()
    except Exception:
        print(type(exc))
        sock.close()
