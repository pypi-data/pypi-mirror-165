# coding: utf8

from enum import Enum, unique


@unique
class UnderlyingType(Enum):
    """
    Underlying type of the option.
    Possible values:
        - Eti
        - Fx
    """

    ETI = "Eti"
    FX = "Fx"
