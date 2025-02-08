
class HttpRequest(object):
    def __init__(self, request_line, headers=None, body=None):
        self.request_line = request_line
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest(request_line={self.request_line}, headers={self.headers}, body={self.body})"

class HttpRequestLine(object):
    def __init__(self, method, uri, version):
        self.method = method
        self.uri = uri
        self.version = version

    def __str__(self):
        return f"HttpRequestLine(method={self.method}, uri={self.uri}, version={self.version})"
