# coding: utf8

from enum import Enum, unique


@unique
class TimeStamp(Enum):
    CLOSE = "Close"
    CLOSE_LONDON5_PM = "CloseLondon5PM"
    CLOSE_NEW_YORK5_PM = "CloseNewYork5PM"
    CLOSE_TOKYO5_PM = "CloseTokyo5PM"
    DEFAULT = "Default"
    OPEN = "Open"
    SETTLE = "Settle"
