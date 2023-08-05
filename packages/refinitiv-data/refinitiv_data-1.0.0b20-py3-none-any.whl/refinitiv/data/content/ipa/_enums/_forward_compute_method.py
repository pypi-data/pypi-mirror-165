# coding: utf8


from enum import Enum, unique


@unique
class ForwardComputeMethod(Enum):
    USE_DIVIDENDS_ONLY = "UseDividendsOnly"
    USE_FORWARD_CRV = "UseForwardCrv"
    USE_FORWARD_CRV_AND_DIVIDENDS = "UseForwardCrvAndDividends"
