# coding: utf8


from enum import Enum, unique


@unique
class CalibrationStrategy(Enum):
    ALL_MATURITY = "AllMaturity"
    DEFAULT = "Default"
    MGB_CALIBRATION = "MGBCalibration"
    MATURITY_BY_MATURITY = "MaturityByMaturity"
