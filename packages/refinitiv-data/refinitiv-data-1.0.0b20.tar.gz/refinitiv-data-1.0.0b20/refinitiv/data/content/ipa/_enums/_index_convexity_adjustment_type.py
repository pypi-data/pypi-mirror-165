# coding: utf8


from enum import Enum, unique


@unique
class IndexConvexityAdjustmentType(Enum):
    NONE = "None"
    BLACK_SCHOLES = "BlackScholes"
    REPLICATION = "Replication"
    LIBOR_SWAP_METHOD = "LiborSwapMethod"
