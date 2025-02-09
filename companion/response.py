from companion.enums import HttpStatus


class HttpResponse(object):
    CRLF = "\r\n"

    def __init__(self, status_code: HttpStatus, version, headers=None, body=None):
        self.status_code_message = status_code.name
        self.status_code = status_code.value
        self.version = version
        self.body = body
        self.headers = headers

    @property
    def bytes(self) -> bytes:
        response = ""
        response += self._build_response_line()
        response += self.CRLF
        if self.headers:
            response += self._build_headers()
            response += self.CRLF
        response += self.CRLF
        response += self._build_response_body()
        return bytes(response, encoding="utf-8")
    
    def _build_response_line(self) -> str:
        return " ".join([self.version, str(self.status_code), self.status_code_message])

    def _build_headers(self) -> str:
        return self.CRLF.join([f"{k}: {v}" for k, v in self.headers.items()])
    
    def _build_response_body(self) -> str:
        return self.body if self.body else ""