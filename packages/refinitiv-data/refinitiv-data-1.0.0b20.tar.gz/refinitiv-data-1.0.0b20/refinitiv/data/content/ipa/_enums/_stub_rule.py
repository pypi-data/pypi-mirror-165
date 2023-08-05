# coding: utf8

from enum import Enum, unique


@unique
class StubRule(Enum):
    ISSUE = "Issue"
    LONG_FIRST_FULL = "LongFirstFull"
    MATURITY = "Maturity"
    SHORT_FIRST_FULL = "ShortFirstFull"
    SHORT_FIRST_PRO_RATA = "ShortFirstProRata"
    SHORT_LAST_PRO_RATA = "ShortLastProRata"
