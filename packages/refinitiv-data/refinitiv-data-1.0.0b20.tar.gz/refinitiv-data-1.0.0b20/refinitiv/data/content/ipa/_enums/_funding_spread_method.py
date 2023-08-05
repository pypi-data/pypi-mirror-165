# coding: utf8


from enum import Enum, unique


@unique
class FundingSpreadMethod(Enum):
    CDS_SPREAD = "CDSSpread"
    LIQUIDITY_SPREAD = "LiquiditySpread"
    PPZ_SPREAD = "PPZSpread"
    PARALLEL_CURVE_SHIFT = "ParallelCurveShift"
    RISKY_D_FS = "RiskyDFs"
    USE_CDS_SPREADS = "UseCDSSpreads"
    USE_Z_SPREAD = "UseZSpread"
    Z_SPREAD = "ZSpread"
