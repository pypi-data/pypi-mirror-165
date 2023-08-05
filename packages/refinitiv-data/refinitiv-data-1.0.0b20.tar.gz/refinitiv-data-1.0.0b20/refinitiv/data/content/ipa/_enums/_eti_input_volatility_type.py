# coding: utf8


from enum import Enum, unique


@unique
class EtiInputVolatilityType(Enum):
    IMPLIED = "Implied"
    QUOTED = "Quoted"
    SETTLE = "Settle"
