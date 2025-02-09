from companion.request import HttpRequest, HttpRequestLine
from companion.enums import HttpMethod


class HttpParser(object):
    """A simple HTTP Parser that turns bytes into HttpRequests"""
    CRLF = "\r\n"

    def __init__(self, data: bytes):
        self.raw_data = data
    
    def parse(self) -> HttpRequest:
        decoded_string = self.raw_data.decode("ascii")
        lines = decoded_string.split(self.CRLF)
        request_line: HttpRequestLine = self._parse_request_line(lines[0])
        headers = self._parse_headers(lines[1:])
        return HttpRequest(request_line, headers)
    
    def _parse_request_line(self, request_line: str) -> HttpRequestLine:
        components = request_line.split()
        method = HttpMethod[components[0]]
        uri = components[1]
        version = components[2]
        return HttpRequestLine(method, uri, version)

    def _parse_headers(self, potential_headers: list[str]):
        headers = {}
        for header in potential_headers:
            if header:
                header_split = header.split(":")
                key = header_split[0]
                val = header_split[1].lstrip()
                headers[key] = val
        return headers
                

