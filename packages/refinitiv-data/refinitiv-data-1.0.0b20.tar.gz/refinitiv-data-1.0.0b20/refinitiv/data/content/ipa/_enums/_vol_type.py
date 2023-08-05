# coding: utf8


from enum import Enum, unique


@unique
class VolType(Enum):
    CALL = "Call"
    PUT = "Put"
