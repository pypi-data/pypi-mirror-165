# coding: utf8

from enum import Enum, unique


@unique
class OptionVolatilityType(Enum):
    HISTORICAL = "Historical"
    IMPLIED = "Implied"
    SVI_SURFACE = "SVISurface"
