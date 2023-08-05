# coding: utf8

from enum import Enum, unique


@unique
class AmortizationType(Enum):
    ANNUITY = "Annuity"
    LINEAR = "Linear"
    NONE = "None"
    SCHEDULE = "Schedule"
