# coding: utf8

from enum import Enum, unique


@unique
class InOrOut(Enum):
    IN = "In"
    OUT = "Out"
