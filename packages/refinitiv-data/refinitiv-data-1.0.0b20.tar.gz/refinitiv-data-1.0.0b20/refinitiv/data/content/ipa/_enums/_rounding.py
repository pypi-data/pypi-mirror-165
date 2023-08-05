# coding: utf8

from enum import Enum, unique


@unique
class Rounding(Enum):
    DEFAULT = "Default"
    EIGHT = "Eight"
    FIVE = "Five"
    FOUR = "Four"
    ONE = "One"
    SEVEN = "Seven"
    SIX = "Six"
    THREE = "Three"
    TWO = "Two"
    UNROUNDED = "Unrounded"
    ZERO = "Zero"
