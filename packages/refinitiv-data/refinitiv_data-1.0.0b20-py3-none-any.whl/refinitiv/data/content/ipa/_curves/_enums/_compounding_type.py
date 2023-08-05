# coding: utf8

from enum import Enum, unique


@unique
class CompoundingType(Enum):
    COMPOUNDED = "Compounded"
    CONTINUOUS = "Continuous"
    DISCOUNTED = "Discounted"
    MONEY_MARKET = "MoneyMarket"
