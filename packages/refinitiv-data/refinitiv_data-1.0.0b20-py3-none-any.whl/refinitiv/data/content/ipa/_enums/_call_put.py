# coding: utf8

from enum import Enum, unique


@unique
class CallPut(Enum):
    CALL = "CALL"
    NONE = "None"
    PUT = "PUT"
