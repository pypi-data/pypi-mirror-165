# coding: utf8

from enum import Enum, unique


@unique
class ZcCurvesOutputs(Enum):
    CONSTITUENTS = "Constituents"
    DETAILED_CURVE_POINT = "DetailedCurvePoint"
