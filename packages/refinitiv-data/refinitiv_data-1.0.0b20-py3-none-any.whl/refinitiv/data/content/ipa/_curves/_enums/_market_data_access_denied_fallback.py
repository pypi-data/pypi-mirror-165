# coding: utf8

from enum import Enum, unique


@unique
class MarketDataAccessDeniedFallback(Enum):
    IGNORE_CONSTITUENTS = "IgnoreConstituents"
    RETURN_ERROR = "ReturnError"
    USE_DELAYED_DATA = "UseDelayedData"
