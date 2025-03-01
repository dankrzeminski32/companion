"""Representation of an HTTP request"""

from companion.enums import HttpMethod


class HttpRequestLine(object):
    """The request line of an HTTP request

    Args:
        method (HttpMethod): the HTTP method (e.g. GET, HEAD)
        target (str): URI for the request
        version (str): HTTP version number
    """

    def __init__(self, method: HttpMethod, target: str, version: str):
        self.method = method
        self.target = target
        self.version = version

    def __str__(self):
        return f"HttpRequestLine(method={self.method}, target={self.target}, version={self.version})"

    def __repr__(self):
        return f"HttpRequestLine(method={self.method}, target={self.target}, version={self.version})"


class HttpRequest(object):
    """HTTP Request object

    Args:
        request_line (HttpRequestLine): the request line of the HTTP request
        headers (dict, optional): HTTP request headers. Defaults to None.
        body (str, optional): HTTP entity body. Defaults to None.
    """

    def __init__(
        self, request_line: HttpRequestLine, headers: dict = None, body: str = None
    ):
        self.request_line = request_line
        self.method = self.request_line.method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest(request_line={self.request_line}, headers={self.headers}, body={self.body})"

    def __repr__(self):
        return f"HttpRequest(request_line={self.request_line}, headers={self.headers}, body={self.body})"
