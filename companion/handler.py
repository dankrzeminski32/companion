from companion.enums import HttpMethod, HttpStatus
from companion.request import HttpRequest
from companion.response import HttpResponse
from pathlib import Path
import mimetypes


class HttpRequestHandler(object):
    def __init__(self, file_directory: Path):
        self.file_directory = file_directory

    def handle(self, http_request: HttpRequest):
        match http_request.method:
            case HttpMethod.GET:
                return self.get(http_request.request_line.target, http_request.headers)
            case HttpMethod.HEAD:
                return self.head(http_request.request_line.target, http_request.headers)

    def get(self, request_target: str, headers: dict):
        clean_request_target = request_target.lstrip("/")
        target_file_or_directory = (self.file_directory / clean_request_target).resolve()
        response_headers = {"Server": "companion"}

        if self.file_directory in target_file_or_directory.parents or target_file_or_directory == self.file_directory:
            if target_file_or_directory.exists():
                if target_file_or_directory.is_dir():
                    if (target_file_or_directory / "index.html").exists():
                        with (target_file_or_directory / "index.html").open("rb") as fp:
                            content = fp.read()
                            response_headers.update(self._get_entity_headers(content, target_file_or_directory / "index.html"))
                            return HttpResponse(HttpStatus.OK, body=content, headers=response_headers)
                else:
                    with target_file_or_directory.open("rb") as fp:
                        content = fp.read()
                        response_headers.update(self._get_entity_headers(content, target_file_or_directory))
                        return HttpResponse(HttpStatus.OK, body=content, headers=response_headers)
        return HttpResponse(HttpStatus.NOT_FOUND, headers=response_headers)

    def _get_entity_headers(self, content: bytes, file_path: Path):
        entity_headers = {"Content-Type": "application/octet-stream"}
        entity_headers["Content-Length"] = len(content)
        content_type, content_encoding = mimetypes.guess_file_type(file_path)
        if content_type:
            entity_headers["Content-Type"] = content_type
        if content_encoding:
            entity_headers["Content-Encoding"] = content_encoding
        return entity_headers

    def head(self, request_target: str, headers: dict):
        ...
