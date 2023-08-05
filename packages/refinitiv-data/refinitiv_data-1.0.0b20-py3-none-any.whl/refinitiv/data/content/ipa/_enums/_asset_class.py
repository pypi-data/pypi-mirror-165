# coding: utf8

from enum import Enum, unique


@unique
class AssetClass(Enum):
    FUTURES = "Futures"
    SWAP = "Swap"
