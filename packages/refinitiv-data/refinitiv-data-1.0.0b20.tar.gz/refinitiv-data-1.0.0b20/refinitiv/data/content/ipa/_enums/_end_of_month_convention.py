# coding: utf8

__all__ = ["EndOfMonthConvention"]

from enum import Enum, unique


@unique
class EndOfMonthConvention(Enum):
    """
    End of month convention.

    The possible values are:
        - Last,
        - Same,
        - Last28,
        - Same28
    """

    LAST = "Last"
    LAST28 = "Last28"
    SAME = "Same"
    SAME28 = "Same28"
