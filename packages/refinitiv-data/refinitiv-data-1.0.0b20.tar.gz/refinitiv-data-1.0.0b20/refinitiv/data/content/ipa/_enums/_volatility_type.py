# coding: utf8

from enum import Enum, unique


@unique
class VolatilityType(Enum):
    FLAT = "Flat"
    TERM_STRUCTURE = "TermStructure"
