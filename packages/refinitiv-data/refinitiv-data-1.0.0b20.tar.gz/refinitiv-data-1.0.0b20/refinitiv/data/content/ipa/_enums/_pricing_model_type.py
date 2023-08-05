# coding: utf8

from enum import Enum, unique


@unique
class PricingModelType(Enum):
    BINOMIAL = "Binomial"
    BLACK_SCHOLES = "BlackScholes"
    LOCAL_VOLATILITY = "LocalVolatility"
    TRINOMIAL = "Trinomial"
    VANNA_VOLGA = "VannaVolga"
    WHALEY = "Whaley"
