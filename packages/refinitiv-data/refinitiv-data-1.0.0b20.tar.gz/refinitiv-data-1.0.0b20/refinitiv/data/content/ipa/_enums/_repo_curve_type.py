# coding: utf8

from enum import Enum, unique


@unique
class RepoCurveType(Enum):
    DEPOSIT_CURVE = "DepositCurve"
    LIBOR_FIXING = "LiborFixing"
    REPO_CURVE = "RepoCurve"
