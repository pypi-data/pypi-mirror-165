# coding: utf8


from enum import Enum, unique


@unique
class DiscountingType(Enum):
    LIBOR_DISCOUNTING = "LiborDiscounting"
    OIS_DISCOUNTING = "OisDiscounting"
