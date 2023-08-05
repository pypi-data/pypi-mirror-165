# coding: utf8

from enum import Enum, unique


@unique
class AdjustInterestToPaymentDate(Enum):
    ADJUSTED = "Adjusted"
    UNADJUSTED = "Unadjusted"
