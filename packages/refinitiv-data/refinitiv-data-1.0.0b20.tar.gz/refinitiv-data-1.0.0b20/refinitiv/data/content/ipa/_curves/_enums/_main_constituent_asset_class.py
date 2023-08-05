# coding: utf8

from enum import Enum, unique


@unique
class MainConstituentAssetClass(Enum):
    FUTURES = "Futures"
    SWAP = "Swap"
