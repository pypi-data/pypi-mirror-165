# coding: utf8


from enum import Enum, unique


@unique
class Method(Enum):
    AMERICAN_MONTE_CARLO = "AmericanMonteCarlo"
    ANALYTIC = "Analytic"
    MONTE_CARLO = "MonteCarlo"
    PDE = "PDE"
    TREE = "Tree"
