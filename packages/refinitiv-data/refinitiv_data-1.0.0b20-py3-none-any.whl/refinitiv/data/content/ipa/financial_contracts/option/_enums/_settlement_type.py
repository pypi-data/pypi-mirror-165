# coding: utf8

from enum import Enum, unique


@unique
class SettlementType(Enum):
    ASSET = "Asset"
    CASH = "Cash"
    UNDEFINED = "Undefined"
