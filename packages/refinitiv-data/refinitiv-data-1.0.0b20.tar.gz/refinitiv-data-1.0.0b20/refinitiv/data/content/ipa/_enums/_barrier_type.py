# coding: utf8

from enum import Enum, unique


@unique
class BarrierType(Enum):
    KNOCK_IN = "KnockIn"
    KNOCK_IN_KNOCK_OUT = "KnockInKnockOut"
    KNOCK_OUT = "KnockOut"
    KNOCK_OUT_KNOCK_IN = "KnockOutKnockIn"
