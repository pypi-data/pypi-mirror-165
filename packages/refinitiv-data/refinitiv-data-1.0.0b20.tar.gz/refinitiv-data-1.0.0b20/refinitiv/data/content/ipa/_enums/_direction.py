# coding: utf8

from enum import Enum, unique


@unique
class Direction(Enum):
    PAID = "Paid"
    RECEIVED = "Received"
