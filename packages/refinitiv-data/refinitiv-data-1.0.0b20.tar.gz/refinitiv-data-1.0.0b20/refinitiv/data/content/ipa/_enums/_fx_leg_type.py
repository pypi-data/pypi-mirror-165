# coding: utf8

from enum import Enum, unique


@unique
class FxLegType(Enum):
    FX_FORWARD = "FxForward"
    FX_NON_DELIVERABLE_FORWARD = "FxNonDeliverableForward"
    FX_SPOT = "FxSpot"
    SWAP_FAR = "SwapFar"
    SWAP_NEAR = "SwapNear"
