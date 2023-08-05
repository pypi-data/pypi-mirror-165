# coding: utf8

from enum import Enum, unique


@unique
class InterestType(Enum):
    FIXED = "Fixed"
    FLOAT = "Float"
    STEPPED = "Stepped"
