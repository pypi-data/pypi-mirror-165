# coding: utf8


from enum import Enum, unique


@unique
class InterpolationMode(Enum):
    CUBIC_DISCOUNT = "CubicDiscount"
    CUBIC_RATE = "CubicRate"
    CUBIC_SPLINE = "CubicSpline"
    FORWARD_MONOTONE_CONVEX = "ForwardMonotoneConvex"
    LINEAR = "Linear"
    LOG = "Log"
