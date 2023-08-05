# coding: utf8

from enum import Enum, unique


@unique
class Seniority(Enum):
    JUNIOR_SUBORDINATED = "JuniorSubordinated"
    NONE = "None"
    PREFERENCE = "Preference"
    SECURED = "Secured"
    SENIOR_UNSECURED = "SeniorUnsecured"
    SUBORDINATED = "Subordinated"
