# coding: utf8

from enum import Enum, unique


@unique
class SwaptionSettlementType(Enum):
    CCP = "CCP"
    CASH = "Cash"
    PHYSICAL = "Physical"
