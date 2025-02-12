from companion.enums import HttpMethod, HttpStatus
from companion.request import HttpRequest
from companion.response import HttpResponse
from pathlib import Path


class HttpRequestHandler(object):
    def __init__(self, file_directory: Path):
        self.file_directory = file_directory

    def handle(self, http_request: HttpRequest):
        match http_request.method:
            case HttpMethod.GET:
                return self.get(http_request.request_line.target, http_request.headers)

    def get(self, request_target: str, headers: dict):
        clean_request_target = request_target.lstrip("/")
        target_file_or_directory = (self.file_directory / clean_request_target).resolve()

        if self.file_directory in target_file_or_directory.parents:
            if target_file_or_directory.exists():
                if target_file_or_directory.is_dir():
                    if (target_file_or_directory / "index.html").exists():
                        with (target_file_or_directory / "index.html").open() as fp:
                            content = fp.read()
                            return HttpResponse(HttpStatus.OK, body=content)
                else:
                    with target_file_or_directory.open() as fp:
                        content = fp.read()
                        return HttpResponse(HttpStatus.OK, body=content)
        return HttpResponse(HttpStatus.NOT_FOUND)

    def head(self, request_target: str, headers: dict):
        ...
