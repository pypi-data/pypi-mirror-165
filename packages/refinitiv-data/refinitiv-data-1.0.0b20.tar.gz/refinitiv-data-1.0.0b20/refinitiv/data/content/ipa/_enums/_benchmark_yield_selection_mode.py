# coding: utf8

from enum import Enum, unique


@unique
class BenchmarkYieldSelectionMode(Enum):
    INTERPOLATE = "Interpolate"
    NEAREST = "Nearest"
