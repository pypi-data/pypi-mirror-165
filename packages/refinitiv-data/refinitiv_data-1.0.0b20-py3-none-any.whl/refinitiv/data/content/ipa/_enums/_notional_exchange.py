# coding: utf8

from enum import Enum, unique


@unique
class NotionalExchange(Enum):
    BOTH = "Both"
    END = "End"
    END_ADJUSTMENT = "EndAdjustment"
    NONE = "None"
    START = "Start"
