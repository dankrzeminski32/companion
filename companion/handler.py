from companion.enums import HttpMethod, HttpStatus
from companion.request import HttpRequest
from companion.response import HttpResponse


class HttpRequestHandler(object):
    def __init__(self, file_directory):
        self.file_directory = file_directory

    def handle(self, http_request: HttpRequest):
        match http_request.method:
            case HttpMethod.GET:
                return self.get(http_request.request_line.target, http_request.headers)

    def get(self, request_target: str, headers: dict):
        return HttpResponse(HttpStatus.OK, "HTTP/1.0")
        ...

    def head(self, request_target: str, headers: dict):
        ...
