# coding: utf8

from enum import Enum, unique


@unique
class IndexConvexityAdjustmentMethod(Enum):
    BLACK_SCHOLES = "BlackScholes"
    LINEAR_SWAP_MODEL = "LinearSwapModel"
    NONE = "None"
    REPLICATION = "Replication"
