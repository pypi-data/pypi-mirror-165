# coding: utf8

from enum import Enum, unique


@unique
class InflationMode(Enum):
    ADJUSTED = "Adjusted"
    DEFAULT = "Default"
    UNADJUSTED = "Unadjusted"
