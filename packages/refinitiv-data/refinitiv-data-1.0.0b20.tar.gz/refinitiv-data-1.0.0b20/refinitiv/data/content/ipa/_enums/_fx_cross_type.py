# coding: utf8

from enum import Enum, unique


@unique
class FxCrossType(Enum):
    FX_FORWARD = "FxForward"
    FX_NON_DELIVERABLE_FORWARD = "FxNonDeliverableForward"
    FX_SPOT = "FxSpot"
    FX_SWAP = "FxSwap"
    FX_TIME_OPTION_FORWARD = "FxTimeOptionForward"
