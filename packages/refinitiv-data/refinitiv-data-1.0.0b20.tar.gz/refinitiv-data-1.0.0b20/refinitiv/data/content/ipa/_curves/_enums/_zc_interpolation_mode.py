# coding: utf8

from enum import Enum, unique


@unique
class ZcInterpolationMode(Enum):
    AKIMA_METHOD = "AkimaMethod"
    CUBIC_DISCOUNT = "CubicDiscount"
    CUBIC_RATE = "CubicRate"
    CUBIC_SPLINE = "CubicSpline"
    FORWARD_MONOTONE_CONVEX = "ForwardMonotoneConvex"
    FRITSCH_BUTLAND_METHOD = "FritschButlandMethod"
    HERMITE = "Hermite"
    KRUGER_METHOD = "KrugerMethod"
    LINEAR = "Linear"
    LOG = "Log"
    MONOTONIC_CUBIC_NATURAL_SPLINE = "MonotonicCubicNaturalSpline"
    MONOTONIC_HERMITE_CUBIC = "MonotonicHermiteCubic"
    TENSION_SPLINE = "TensionSpline"
