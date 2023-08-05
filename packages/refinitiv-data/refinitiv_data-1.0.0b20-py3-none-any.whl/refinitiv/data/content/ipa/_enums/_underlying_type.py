# coding: utf8

from enum import Enum, unique


@unique
class UnderlyingType(Enum):
    ETI = "Eti"
    FX = "Fx"
    CAP = "Cap"
    SWAPTION = "Swaption"
