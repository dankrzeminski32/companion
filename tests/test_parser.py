from companion.parser import HttpParser

GET_REQ_WITH_HEADERS = b"Get /mysite/index.html HTTP/1.1\r\nHost: 10.101.101.10\r\nAccept: */*\r\n\r\n"

def test_parse_get_request():
    parser = HttpParser(GET_REQ_WITH_HEADERS)
    result = parser.parse()
    assert result.request_line.method == "Get"
    assert result.request_line.uri == "/mysite/index.html"
    assert result.request_line.version == "HTTP/1.1"
    assert result.headers == {"Host": "10.101.101.10", "Accept": "*/*"}
    assert result.body == None