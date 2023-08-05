# coding: utf8

__all__ = ["PeriodType"]

from enum import Enum, unique


@unique
class PeriodType(Enum):
    """
    The method we chose to count the period of time:

    The possible values are:
        - WorkingDay (consider only working days),
        - NonWorkingDay (consider only non working days),
        - Day (consider all days),
        - Year (consider year),
        - NearestTenor (returns the nearest tenor for the given period)
    """

    WORKING_DAY = "WorkingDay"
    NON_WORKING_DAY = "NonWorkingDay"
    DAY = "Day"
    YEAR = "Year"
    NEAREST_TENOR = "NearestTenor"
