# coding: utf8

from enum import Enum, unique


@unique
class SurfaceOutputs(Enum):
    HEADERS = "Headers"
    DATATYPE = "DataType"
    DATA = "Data"
    STATUSES = "Statuses"
    FORWARD_CURVE = "ForwardCurve"
    DIVIDENDS = "Dividends"
    INTEREST_RATE_CURVE = "InterestRateCurve"
    GOODNESS_OF_FIT = "GoodnessOfFit"
    UNDERLYING_SPOT = "UnderlyingSpot"
    DISCOUNT_CURVE = "DiscountCurve"
    MONEYNESS_STRIKE = "MoneynessStrike"
