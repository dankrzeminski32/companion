"""Support handling of a generic HTTP request"""

from companion.enums import HttpMethod, HttpStatus
from companion.request import HttpRequest
from companion.response import HttpResponse
from pathlib import Path
import mimetypes
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class HttpRequestHandler(object):
    """Handles generic HTTP requests

    Args:
        file_directory (Path): path to static content (e.g. HTML, PNG)
    """

    def __init__(self, file_directory: Path):
        self.file_directory = file_directory

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Handles a generic HttpRequest

        Args:
            http_request (HttpRequest): the HTTP request in context

        Returns:
            HttpResponse: a valid HTTP response
        """
        match http_request.method:
            case HttpMethod.GET:
                return self.get(http_request.request_line.target, http_request.headers)
            case HttpMethod.HEAD:
                return self.head(http_request.request_line.target, http_request.headers)

    def get(self, request_target: str, headers: dict) -> HttpResponse:
        """implements the GET method of the HTTP protocol

        Args:
            request_target (str): target file or directory to retrieve
            headers (dict): request headers

        Returns:
            HttpResponse: a valid HTTP response
        """
        content, headers = self._get_file_content_and_headers(request_target, headers)
        if content and headers:
            return HttpResponse(HttpStatus.OK, headers=headers, body=content)
        return HttpResponse(HttpStatus.NOT_FOUND, headers=headers)

    def head(self, request_target: str, headers: dict):
        """implements the HEAD method of the HTTP protocol

        Args:
            request_target (str): target file or directory to retrieve
            headers (dict): request headers

        Returns:
            HttpResponse: a valid HTTP response
        """
        _, headers = self._get_file_content_and_headers(request_target, headers)
        if headers:
            return HttpResponse(HttpStatus.OK, headers=headers)
        return HttpResponse(HttpStatus.NOT_FOUND, headers=headers)

    def _get_file_content_and_headers(self, request_target: str, headers: dict):
        clean_request_target = request_target.lstrip("/")
        target_file_or_directory = (
            self.file_directory / clean_request_target
        ).resolve()
        logger.info(f"Attempting to serve file {target_file_or_directory}")
        response_headers = {"Server": "companion"}

        if (
            self.file_directory in target_file_or_directory.parents
            or target_file_or_directory == self.file_directory
        ):
            if target_file_or_directory.exists():
                if target_file_or_directory.is_dir():
                    if (target_file_or_directory / "index.html").exists():
                        with (target_file_or_directory / "index.html").open("rb") as fp:
                            content = fp.read()
                            response_headers.update(
                                self._get_entity_headers(
                                    content, target_file_or_directory / "index.html"
                                )
                            )
                            return content, response_headers
                else:
                    with target_file_or_directory.open("rb") as fp:
                        content = fp.read()
                        response_headers.update(
                            self._get_entity_headers(content, target_file_or_directory)
                        )
                        return content, response_headers
        return None, response_headers

    def _get_entity_headers(self, content: bytes, file_path: Path):
        entity_headers = {"Content-Type": "application/octet-stream"}
        entity_headers["Content-Length"] = len(content)
        content_type, content_encoding = mimetypes.guess_file_type(file_path)
        if content_type:
            entity_headers["Content-Type"] = content_type
        if content_encoding:
            entity_headers["Content-Encoding"] = content_encoding
        return entity_headers
