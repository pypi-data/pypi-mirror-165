# coding: utf8

from enum import Enum, unique


@unique
class FxSwapCalculationMethod(Enum):
    FX_SWAP = "FxSwap"
    FX_SWAP_IMPLIED_FROM_DEPOSIT = "FxSwapImpliedFromDeposit"
