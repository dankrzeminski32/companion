"""Stores enumerations of Http-related data"""

from enum import Enum, auto


class HttpMethod(Enum):
    """Methods from HTTP 1.0"""

    GET = auto()
    HEAD = auto()


class HttpStatus(Enum):
    """Status codes from HTTP 1.0"""

    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")

    def __new__(cls, value, message):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.message = message
        return obj
