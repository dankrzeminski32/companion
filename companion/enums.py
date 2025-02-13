from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    HEAD = auto()


class HttpStatus(Enum):
    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")

    def __new__(cls, value, message):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.message = message
        return obj
