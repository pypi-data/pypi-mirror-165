# coding: utf8

from enum import Enum, unique


@unique
class AverageType(Enum):
    ARITHMETIC_RATE = "ArithmeticRate"
    ARITHMETIC_STRIKE = "ArithmeticStrike"
    GEOMETRIC_RATE = "GeometricRate"
    GEOMETRIC_STRIKE = "GeometricStrike"
