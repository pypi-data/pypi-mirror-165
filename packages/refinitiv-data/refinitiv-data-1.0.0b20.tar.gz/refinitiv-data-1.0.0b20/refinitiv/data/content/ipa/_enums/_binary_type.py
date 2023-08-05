# coding: utf8

from enum import Enum, unique


@unique
class BinaryType(Enum):
    DIGITAL = "Digital"
    NO_TOUCH = "NoTouch"
    NONE = "None"
    ONE_TOUCH = "OneTouch"
