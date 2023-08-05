# coding: utf8

from enum import Enum, unique


@unique
class CreditSpreadType(Enum):
    FLAT_SPREAD = "FlatSpread"
    TERM_STRUCTURE = "TermStructure"
