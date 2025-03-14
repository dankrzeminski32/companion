"""Representation of an HTTP response"""

from companion.enums import HttpStatus


class HttpResponse(object):
    """Http Response object

    Args:
        status_code (HttpStatus): status code of the HTTP response
        version (str, optional): HTTP version number. Defaults to "HTTP/1.0".
        headers (_type_, optional): HTTP headers. Defaults to None.
        body (_type_, optional): HTTP entity body. Defaults to None.
    """

    CRLF = "\r\n"

    def __init__(
        self, status_code: HttpStatus, *, version="HTTP/1.0", headers=None, body=None
    ):
        self.status_code_message = status_code.message
        self.status_code = status_code.value
        self.version = version
        self.body = body
        self.headers = headers

    @property
    def bytes(self) -> bytes:
        """Converts response into bytes

        Returns:
            bytes: bytes of the HTTP response
        """
        response = ""
        response += self._build_response_line()
        response += self.CRLF
        if self.headers:
            response += self._build_headers()
            response += self.CRLF
        response += self.CRLF
        return bytes(response, encoding="ascii") + self._build_response_body()

    def _build_response_line(self) -> str:
        return " ".join([self.version, str(self.status_code), self.status_code_message])

    def _build_headers(self) -> str:
        return self.CRLF.join([f"{k}: {v}" for k, v in self.headers.items()])

    def _build_response_body(self) -> str:
        return self.body if self.body else b""

    def __str__(self):
        return f"HttpResponse(status_code={self.status_code}, headers={self.headers}, body={self.body})"

    def __repr__(self):
        return f"HttpResponse(version={self.version}, message={self.status_code_message}, status_code={self.status_code}, headers={self.headers}, body={self.body})"
