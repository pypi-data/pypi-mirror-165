# coding: utf8

from enum import Enum, unique


@unique
class BusinessDayConvention(Enum):
    BBSW_MODIFIED_FOLLOWING = "BbswModifiedFollowing"
    EVERY_THIRD_WEDNESDAY = "EveryThirdWednesday"
    MODIFIED_FOLLOWING = "ModifiedFollowing"
    NEXT_BUSINESS_DAY = "NextBusinessDay"
    NO_MOVING = "NoMoving"
    PREVIOUS_BUSINESS_DAY = "PreviousBusinessDay"
