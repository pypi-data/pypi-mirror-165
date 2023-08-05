# coding: utf8

from enum import Enum, unique


@unique
class IndexSpreadCompoundingMethod(Enum):
    ISDA_COMPOUNDING = "IsdaCompounding"
    ISDA_FLAT_COMPOUNDING = "IsdaFlatCompounding"
    NO_COMPOUNDING = "NoCompounding"
