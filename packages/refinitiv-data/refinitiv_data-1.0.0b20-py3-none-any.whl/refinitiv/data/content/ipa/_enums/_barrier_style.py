# coding: utf8

from enum import Enum, unique


@unique
class BarrierStyle(Enum):
    AMERICAN = "American"
    EUROPEAN = "European"
    NONE = "None"
