# coding: utf8

from enum import Enum, unique


@unique
class ExerciseStyle(Enum):
    AMER = "AMER"
    BERM = "BERM"
    EURO = "EURO"
