# coding: utf8

from enum import Enum, unique


@unique
class SwaptionType(Enum):
    PAYER = "Payer"
    RECEIVER = "Receiver"
