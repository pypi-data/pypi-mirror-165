# coding: utf8

from enum import Enum, unique


@unique
class IndexCompoundingMethod(Enum):
    ADJUSTED_COMPOUNDED = "AdjustedCompounded"
    AVERAGE = "Average"
    COMPOUNDED = "Compounded"
    CONSTANT = "Constant"
    MEXICAN_COMPOUNDED = "MexicanCompounded"
