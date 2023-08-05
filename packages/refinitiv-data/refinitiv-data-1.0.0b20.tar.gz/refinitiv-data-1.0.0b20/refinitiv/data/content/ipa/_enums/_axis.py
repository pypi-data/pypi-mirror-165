# coding: utf8

__all__ = ["Axis"]

from enum import Enum, unique


@unique
class Axis(Enum):
    """
    The enumerate that specifies the unit for the axis.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    DATE = "Date"
    DELTA = "Delta"
    EXPIRY = "Expiry"
    MONEYNESS = "Moneyness"
    STRIKE = "Strike"
    TENOR = "Tenor"
