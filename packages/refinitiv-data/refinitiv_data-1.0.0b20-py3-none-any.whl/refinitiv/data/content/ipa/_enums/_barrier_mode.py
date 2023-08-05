# coding: utf8

from enum import Enum, unique


@unique
class BarrierMode(Enum):
    AMERICAN = "American"
    EARLY_END_WINDOW = "EarlyEndWindow"
    EUROPEAN = "European"
    FORWARD_START_WINDOW = "ForwardStartWindow"
    UNDEFINED = "Undefined"
