# coding: utf8

from enum import Enum, unique


@unique
class IndexConvexityAdjustmentIntegrationMethod(Enum):
    RIEMANN_SUM = "RiemannSum"
    RUNGE_KUTTA = "RungeKutta"
