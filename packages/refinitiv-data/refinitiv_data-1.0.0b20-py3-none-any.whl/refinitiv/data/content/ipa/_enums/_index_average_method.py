# coding: utf8

from enum import Enum, unique


@unique
class IndexAverageMethod(Enum):
    ARITHMETIC_AVERAGE = "ArithmeticAverage"
    COMPOUNDED_ACTUAL = "CompoundedActual"
    COMPOUNDED_AVERAGE_RATE = "CompoundedAverageRate"
    DAILY_COMPOUNDED_AVERAGE = "DailyCompoundedAverage"
