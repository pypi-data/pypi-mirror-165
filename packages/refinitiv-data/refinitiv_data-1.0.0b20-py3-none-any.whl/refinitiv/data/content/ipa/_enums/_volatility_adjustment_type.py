# coding: utf8


from enum import Enum, unique


@unique
class VolatilityAdjustmentType(Enum):
    CONSTANT_CAP = "ConstantCap"
    CONSTANT_CAPLET = "ConstantCaplet"
    NORMALIZED_CAP = "NormalizedCap"
    NORMALIZED_CAPLET = "NormalizedCaplet"
    PB_UNDEFINED = "PbUndefined"
    SHIFTED_CAP = "ShiftedCap"
