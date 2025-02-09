from companion.response import HttpResponse
from companion.enums import HttpStatus

def test_response_no_headers_no_body():
    resp = HttpResponse(HttpStatus.OK, "HTTP/1.0")
    assert resp.bytes == b"HTTP/1.0 200 OK\r\n\r\n"

def test_response_1_header_no_body():
    resp = HttpResponse(HttpStatus.OK, "HTTP/1.0", {"test": "case"})
    assert resp.bytes == b"HTTP/1.0 200 OK\r\ntest: case\r\n\r\n"

def test_response_2_header_no_body():
    resp = HttpResponse(HttpStatus.OK, "HTTP/1.0", {"test": "case", "test2": "case2"})
    assert resp.bytes == b"HTTP/1.0 200 OK\r\ntest: case\r\ntest2: case2\r\n\r\n"

def test_response_2_header_body():
    resp = HttpResponse(HttpStatus.OK, "HTTP/1.0", {"test": "case", "test2": "case2"}, "<div>hello</div>")
    assert resp.bytes == b"HTTP/1.0 200 OK\r\ntest: case\r\ntest2: case2\r\n\r\n<div>hello</div>"