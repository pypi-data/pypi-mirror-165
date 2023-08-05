# coding: utf8


from enum import Enum, unique


@unique
class SwaptionVolatilityType(Enum):
    ATM_SURFACE = "AtmSurface"
    SABR_VOLATILITY_CUBE = "SabrVolatilityCube"
