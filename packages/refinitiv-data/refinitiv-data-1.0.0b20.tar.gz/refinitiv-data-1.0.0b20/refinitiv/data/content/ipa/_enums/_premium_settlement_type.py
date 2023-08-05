# coding: utf8

from enum import Enum, unique


@unique
class PremiumSettlementType(Enum):
    FORWARD = "Forward"
    SCHEDULE = "Schedule"
    SPOT = "Spot"
