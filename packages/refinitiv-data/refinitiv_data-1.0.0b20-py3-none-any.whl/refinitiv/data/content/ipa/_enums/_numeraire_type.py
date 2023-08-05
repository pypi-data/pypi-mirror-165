# coding: utf8


from enum import Enum, unique


@unique
class NumeraireType(Enum):
    CASH = "Cash"
    ROLLING_EVENT = "RollingEvent"
    ROLLING_PAYMENT = "RollingPayment"
    TERMINAL_EVENT_ZC = "TerminalEventZc"
    TERMINAL_ZC = "TerminalZc"
