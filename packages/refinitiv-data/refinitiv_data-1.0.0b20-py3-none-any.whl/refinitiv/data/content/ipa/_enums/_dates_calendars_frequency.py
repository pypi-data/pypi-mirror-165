# coding: utf8

__all__ = ["DateScheduleFrequency"]

from enum import Enum, unique


@unique
class DateScheduleFrequency(Enum):
    """
    The frequency of dates in the predefined period. The possible values are:

    The possible values are:
        - Daily,
        - Weekly,
        - BiWeekly,
        - Monthly,
    """

    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "BiWeekly"
    MONTHLY = "Monthly"
