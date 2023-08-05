# coding: utf8

from enum import Enum, unique


@unique
class BuySell(Enum):
    BUY = "Buy"
    SELL = "Sell"
