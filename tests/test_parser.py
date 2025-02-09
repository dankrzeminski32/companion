from companion.parser import HttpParser
from companion.enums import HttpMethod
from companion.request import HttpRequest, HttpRequestLine

GET_REQ_WITH_HEADERS = b"GET /mysite/index.html HTTP/1.1\r\nHost: 10.101.101.10\r\nAccept: */*\r\n\r\n"

def test_parse_get_request():
    parser = HttpParser(GET_REQ_WITH_HEADERS)
    result = parser.parse()
    assert isinstance(result, HttpRequest) is True
    assert isinstance(result.request_line, HttpRequestLine) is True
    assert result.request_line.method == HttpMethod.GET
    assert result.request_line.target == "/mysite/index.html"
    assert result.request_line.version == "HTTP/1.1"
    assert result.headers == {"Host": "10.101.101.10", "Accept": "*/*"}
    assert result.body is None

