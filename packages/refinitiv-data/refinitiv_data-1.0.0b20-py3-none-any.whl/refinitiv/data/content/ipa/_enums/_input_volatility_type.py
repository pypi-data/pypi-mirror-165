# coding: utf8


from enum import Enum, unique


@unique
class InputVolatilityType(Enum):
    DEFAULT = "Default"
    LOG_NORMAL_VOLATILITY = "LogNormalVolatility"
    NORMALIZED_VOLATILITY = "NormalizedVolatility"
