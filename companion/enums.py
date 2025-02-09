from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    HEAD = auto()


class HttpStatus(Enum):
    OK = 200