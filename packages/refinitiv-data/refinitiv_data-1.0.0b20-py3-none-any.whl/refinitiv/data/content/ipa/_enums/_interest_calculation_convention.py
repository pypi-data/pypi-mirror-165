# coding: utf8

from enum import Enum, unique


@unique
class InterestCalculationConvention(Enum):
    BOND_BASIS = "BondBasis"
    MONEY_MARKET = "MoneyMarket"
    NONE = "None"
