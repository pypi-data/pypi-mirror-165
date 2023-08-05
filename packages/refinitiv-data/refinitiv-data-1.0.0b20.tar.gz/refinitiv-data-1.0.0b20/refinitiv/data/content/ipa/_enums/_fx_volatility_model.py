# coding: utf8


from enum import Enum, unique


@unique
class FxVolatilityModel(Enum):
    CUBIC_SPLINE = "CubicSpline"
    SABR = "SABR"
    SVI = "SVI"
    TWIN_LOGNORMAL = "TwinLognormal"
