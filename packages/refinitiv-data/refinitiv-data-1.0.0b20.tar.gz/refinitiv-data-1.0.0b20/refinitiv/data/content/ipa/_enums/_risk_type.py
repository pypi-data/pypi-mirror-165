# coding: utf8


from enum import Enum, unique


@unique
class RiskType(Enum):
    INTEREST_RATE = "InterestRate"
