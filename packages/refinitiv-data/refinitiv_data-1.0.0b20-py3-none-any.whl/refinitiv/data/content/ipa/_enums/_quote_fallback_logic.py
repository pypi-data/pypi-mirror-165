# coding: utf8

from enum import Enum, unique


@unique
class QuoteFallbackLogic(Enum):
    BEST_FIELD = "BestField"
    NONE = "None"
