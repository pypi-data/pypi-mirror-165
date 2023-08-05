# coding: utf8

from enum import Enum, unique


@unique
class VolatilityTermStructureType(Enum):
    HISTORICAL = "Historical"
    IMPLIED = "Implied"
