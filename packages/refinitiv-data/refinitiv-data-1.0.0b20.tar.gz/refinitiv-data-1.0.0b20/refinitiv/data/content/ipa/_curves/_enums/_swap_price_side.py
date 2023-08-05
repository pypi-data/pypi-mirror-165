# coding: utf8

from enum import Enum, unique


@unique
class SwapPriceSide(Enum):
    ASK = "Ask"
    BID = "Bid"
    MID = "Mid"
