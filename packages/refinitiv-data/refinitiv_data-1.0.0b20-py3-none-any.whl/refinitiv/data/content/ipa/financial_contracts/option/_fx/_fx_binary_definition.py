# coding: utf8

from typing import Optional

from .._base import BinaryDefinition
from .._enums import (
    FxBinaryType,
)


class FxBinaryDefinition(BinaryDefinition):
    """
    Parameters
    ----------
    binary_type : FxBinaryType, optional
        The type of a binary option. the possible values are:
        - onetouchimmediate: the option expires in-the-money if the trigger is reached
          at any time prior to option expiration.the option premium is paid immediately.
        - onetouchdeferred: the option expires in-the-money if the trigger is reached at
          any time prior to option expiration. the option premium payment is deferred.
        - notouch: the option expires in-the-money if the trigger is not reached prior
          to expiration.
        - digital: the option expires in-the-money if the trigger is reached at the
          option expiry date. mandatory for binary options.
    payout_amount : float, optional
        The payout amount of the option. the default value is '1,000,000'.
    payout_ccy : str, optional
        The trade currency, which is either a domestic or foreign currency. either
        payoutccy or settlementtype can be used at a time. payoutccy="foreign currency"
        is equivalent to settlementtype ="physical", and payoutccy="domestic currency"
        is equivalent to settlementtype ="cash". the value is expressed in iso 4217
        alphabetical format (e.g. 'usd').
    trigger : float, optional
        The trigger of the binary option.
    """

    def __init__(
        self,
        binary_type: Optional[FxBinaryType] = None,
        payout_amount: Optional[float] = None,
        payout_ccy: Optional[str] = None,
        trigger: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.binary_type = binary_type
        self.payout_amount = payout_amount
        self.payout_ccy = payout_ccy
        self.trigger = trigger

    @property
    def binary_type(self):
        """
        Binary Type of the digital option
        :return: enum FxBinaryType
        """
        return self._get_enum_parameter(FxBinaryType, "binaryType")

    @binary_type.setter
    def binary_type(self, value):
        self._set_enum_parameter(FxBinaryType, "binaryType", value)

    @property
    def payout_amount(self):
        """
        Payout of the binary option. Default
        :return: float
        """
        return self._get_parameter("payoutAmount")

    @payout_amount.setter
    def payout_amount(self, value):
        self._set_parameter("payoutAmount", value)

    @property
    def payout_ccy(self):
        """
        Payout Currency of the binary option. Default
        :return: str
        """
        return self._get_parameter("payoutCcy")

    @payout_ccy.setter
    def payout_ccy(self, value):
        self._set_parameter("payoutCcy", value)

    @property
    def trigger(self):
        """
        trigger of the binary option.
        :return: float
        """
        return self._get_parameter("trigger")

    @trigger.setter
    def trigger(self, value):
        self._set_parameter("trigger", value)
