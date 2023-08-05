# coding: utf8

from enum import Enum, unique


@unique
class ImpliedDepositDateConvention(Enum):
    FX_MARKET_CONVENTION = "FxMarketConvention"
    MONEY_MARKET_CONVENTION = "MoneyMarketConvention"
