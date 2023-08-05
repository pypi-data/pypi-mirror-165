# coding: utf8

from enum import Enum, unique


@unique
class FxBinaryType(Enum):
    DIGITAL = "Digital"
    NO_TOUCH = "NoTouch"
    NONE = "None"
    ONE_TOUCH_DEFERRED = "OneTouchDeferred"
    ONE_TOUCH_IMMEDIATE = "OneTouchImmediate"
