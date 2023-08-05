# coding: utf8

from enum import Enum, unique


@unique
class ProjectedIndexCalculationMethod(Enum):
    CONSTANT_COUPON_PAYMENT = "ConstantCouponPayment"
    CONSTANT_INDEX = "ConstantIndex"
    FORWARD_INDEX = "ForwardIndex"
