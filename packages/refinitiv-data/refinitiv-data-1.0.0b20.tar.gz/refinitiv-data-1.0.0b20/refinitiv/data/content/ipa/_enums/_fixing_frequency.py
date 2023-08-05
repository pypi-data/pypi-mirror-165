# coding: utf8

from enum import Enum, unique


@unique
class FixingFrequency(Enum):
    DAILY = "Daily"
    BI_WEEKLY = "BiWeekly"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUATERLY = "Quaterly"
    SEMI_ANNUAL = "SemiAnnual"
    ANNUAL = "Annual"
