# coding: utf8


from enum import Enum, unique


@unique
class DividendExtrapolation(Enum):
    CST_EXTRAPOL = "Cst_Extrapol"
    LINEAR_EXTRAPOL = "Linear_Extrapol"
    POWER_GROWTH_EXTRAPOL = "PowerGrowth_Extrapol"
