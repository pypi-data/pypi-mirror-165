# coding: utf8

from enum import Enum, unique


@unique
class DateRollingConvention(Enum):
    LAST = "Last"
    LAST28 = "Last28"
    SAME = "Same"
    SAME28 = "Same28"
