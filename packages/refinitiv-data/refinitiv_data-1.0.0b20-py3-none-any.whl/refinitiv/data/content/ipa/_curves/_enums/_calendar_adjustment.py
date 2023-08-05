# coding: utf8

from enum import Enum, unique


@unique
class CalendarAdjustment(Enum):
    FALSE = False
    NULL = None
    WEEKEND = "Weekend"
    CALENDAR = "Calendar"
