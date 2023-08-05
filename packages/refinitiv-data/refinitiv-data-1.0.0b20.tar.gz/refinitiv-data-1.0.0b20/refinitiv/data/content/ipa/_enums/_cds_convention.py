# coding: utf8

from enum import Enum, unique


@unique
class CdsConvention(Enum):
    ISDA = "ISDA"
    USER_DEFINED = "UserDefined"
