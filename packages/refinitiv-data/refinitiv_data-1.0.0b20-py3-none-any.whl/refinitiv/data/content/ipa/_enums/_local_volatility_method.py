# coding: utf8


from enum import Enum, unique


@unique
class LocalVolatilityMethod(Enum):
    BEST_SMILE = "BestSmile"
    CONVEX_SMILE = "ConvexSmile"
    PARABOLA_SMOOTH = "ParabolaSmooth"
    PARABOLA_WITHOUT_EXTRAPOL = "ParabolaWithoutExtrapol"
    RATIONAL_SMOOTH = "RationalSmooth"
    RATIONAL_WITHOUT_EXTRAPOL = "RationalWithoutExtrapol"
