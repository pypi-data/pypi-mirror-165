# coding: utf8

from enum import Enum, unique


@unique
class IndexObservationMethod(Enum):
    LOOKBACK = "Lookback"
    MIXED = "Mixed"
    PERIOD_SHIFT = "PeriodShift"
