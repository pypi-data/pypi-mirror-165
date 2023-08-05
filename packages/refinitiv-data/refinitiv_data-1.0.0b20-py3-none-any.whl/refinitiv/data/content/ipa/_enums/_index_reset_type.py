# coding: utf8

from enum import Enum, unique


@unique
class IndexResetType(Enum):
    IN_ADVANCE = "InAdvance"
    IN_ARREARS = "InArrears"
