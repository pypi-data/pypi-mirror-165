# coding: utf8

from enum import Enum, unique


@unique
class ExerciseScheduleType(Enum):
    FIXED_LEG = "FixedLeg"
    FLOAT_LEG = "FloatLeg"
    USER_DEFINED = "UserDefined"
