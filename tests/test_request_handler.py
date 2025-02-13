from companion.handler import HttpRequestHandler

def test_GET_request_for_nonexistant_file_returns_404(tmp_path):
    handler = HttpRequestHandler(tmp_path)
    resp = handler.get("/doesnotexist", {})
    assert resp.status_code == 404
    assert resp.status_code_message == "Not Found"
    assert resp.body is None
    assert resp.bytes == b"HTTP/1.0 404 Not Found\r\n\r\n"

def test_GET_request_for_existing_html_file_returns_200_resp(tmp_path):
    handler = HttpRequestHandler(tmp_path)
    open(tmp_path / "doesexist.html", "wb").write(b"<div>test</div>")
    resp = handler.get("/doesexist.html", {})
    assert resp.status_code == 200
    assert resp.status_code_message == "OK"
    assert resp.body == b"<div>test</div>"
    assert resp.bytes == b"HTTP/1.0 200 OK\r\n\r\n<div>test</div>"

def test_get_request_for_path_with_default_indexhtml_returns_200_resp(tmp_path):
    handler = HttpRequestHandler(tmp_path)
    open(tmp_path / "index.html", "wb").write(b"<div>test</div>")
    resp = handler.get("/", {})
    assert resp.status_code == 200
    assert resp.status_code_message == "OK"
    assert resp.body == b"<div>test</div>"
    assert resp.bytes == b"HTTP/1.0 200 OK\r\n\r\n<div>test</div>"

def test_get_request_with_target_outside_folder_returns_404(tmp_path):
    handler = HttpRequestHandler(tmp_path)
    open(tmp_path / "index.html", "wb").write(b"<div>test</div>")
    resp = handler.get("/../", {})
    assert resp.status_code == 404
    assert resp.status_code_message == "Not Found"
    assert resp.body is None
    assert resp.bytes == b"HTTP/1.0 404 Not Found\r\n\r\n"
