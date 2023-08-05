# coding: utf8

from enum import Enum, unique


@unique
class AmericanMonteCarloMethod(Enum):
    ANDERSEN = "Andersen"
    LONGSTAFF_SCHWARTZ = "LongstaffSchwartz"
