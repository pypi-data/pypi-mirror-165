# coding: utf8


from enum import Enum, unique


@unique
class EquityDividendType(Enum):
    DEFAULT = "Default"
    DISCRETE = "Discrete"
    YIELD = "Yield"
