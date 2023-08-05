# coding: utf8

from enum import Enum, unique


@unique
class TenorReferenceDate(Enum):
    SPOT_DATE = "SpotDate"
    VALUATION_DATE = "ValuationDate"
