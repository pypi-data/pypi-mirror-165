# coding: utf8

from enum import Enum, unique


@unique
class MoneynessType(Enum):
    FWD = "Fwd"
    SIGMA = "Sigma"
    SPOT = "Spot"
