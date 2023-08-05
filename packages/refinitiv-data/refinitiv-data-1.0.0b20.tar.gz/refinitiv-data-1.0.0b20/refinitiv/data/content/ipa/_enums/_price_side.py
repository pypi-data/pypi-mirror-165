# coding: utf8

from enum import Enum, unique


@unique
class PriceSide(Enum):
    ASK = "Ask"
    BID = "Bid"
    LAST = "Last"
    MID = "Mid"
