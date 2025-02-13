from companion.enums import HttpMethod


class HttpRequestLine(object):
    def __init__(self, method: HttpMethod, target: str, version: str):
        self.method = method
        self.target = target
        self.version = version

    def __str__(self):
        return f"HttpRequestLine(method={self.method}, target={self.target}, version={self.version})"

    def __repr__(self):
        return f"HttpRequestLine(method={self.method}, target={self.target}, version={self.version})"



class HttpRequest(object):
    def __init__(self, request_line: HttpRequestLine, headers=None, body=None):
        self.request_line = request_line
        self.method = self.request_line.method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"HttpRequest(request_line={self.request_line}, headers={self.headers}, body={self.body})"

    def __repr__(self):
        return f"HttpRequest(request_line={self.request_line}, headers={self.headers}, body={self.body})"