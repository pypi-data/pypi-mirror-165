# coding: utf8

from enum import Enum, unique


@unique
class AmortizationFrequency(Enum):
    EVERY12TH_COUPON = "Every12thCoupon"
    EVERY2ND_COUPON = "Every2ndCoupon"
    EVERY3RD_COUPON = "Every3rdCoupon"
    EVERY4TH_COUPON = "Every4thCoupon"
    EVERY_COUPON = "EveryCoupon"
    ONCE = "Once"
