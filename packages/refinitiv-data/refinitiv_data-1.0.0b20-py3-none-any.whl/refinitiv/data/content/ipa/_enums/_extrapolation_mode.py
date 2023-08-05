# coding: utf8


from enum import Enum, unique


@unique
class ExtrapolationMode(Enum):
    CONSTANT = "Constant"
    LINEAR = "Linear"
    NONE = "None"
