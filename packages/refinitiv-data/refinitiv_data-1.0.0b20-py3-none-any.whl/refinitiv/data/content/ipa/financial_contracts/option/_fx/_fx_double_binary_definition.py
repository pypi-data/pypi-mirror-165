# coding: utf8

from typing import Optional

from .._enums import DoubleBinaryType
from ..._instrument_definition import ObjectDefinition


class FxDoubleBinaryDefinition(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    double_binary_type : DoubleBinaryType, optional
        The type of a double binary option. the possible values are:
        - doublenotouch: the option expires in-the-money if the price of the underlying
          asset fails to breach either the lower trigger or the upper trigger at any
          time prior to option expiration.
    payout_amount : float, optional
        The payout amount of the option. the default value is '1,000,000'.
    payout_ccy : str, optional
        The trade currency, which is either a domestic or foreign currency. either
        payoutccy or settlementtype can be used at a time. payoutccy="foreign currency"
        is equivalent to settlementtype ="physical", and payoutccy="domestic currency"
        is equivalent to settlementtype ="cash". the value is expressed in iso 4217
        alphabetical format (e.g. 'usd').
    trigger_down : float, optional
        The lower trigger of the binary option.
    trigger_up : float, optional
        The upper trigger of the binary option.
    """

    def __init__(
        self,
        double_binary_type: Optional[DoubleBinaryType] = None,
        payout_amount: Optional[float] = None,
        payout_ccy: Optional[str] = None,
        trigger_down: Optional[float] = None,
        trigger_up: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.double_binary_type = double_binary_type
        self.payout_amount = payout_amount
        self.payout_ccy = payout_ccy
        self.trigger_down = trigger_down
        self.trigger_up = trigger_up

    @property
    def double_binary_type(self):
        """
        The type of a double binary option. the possible values are:
        - doublenotouch: the option expires in-the-money if the price of the underlying
          asset fails to breach either the lower trigger or the upper trigger at any
          time prior to option expiration.
        :return: enum DoubleBinaryType
        """
        return self._get_enum_parameter(DoubleBinaryType, "doubleBinaryType")

    @double_binary_type.setter
    def double_binary_type(self, value):
        self._set_enum_parameter(DoubleBinaryType, "doubleBinaryType", value)

    @property
    def payout_amount(self):
        """
        The payout amount of the option. the default value is '1,000,000'.
        :return: float
        """
        return self._get_parameter("payoutAmount")

    @payout_amount.setter
    def payout_amount(self, value):
        self._set_parameter("payoutAmount", value)

    @property
    def payout_ccy(self):
        """
        The trade currency, which is either a domestic or foreign currency. either
        payoutccy or settlementtype can be used at a time. payoutccy="foreign currency"
        is equivalent to settlementtype ="physical", and payoutccy="domestic currency"
        is equivalent to settlementtype ="cash". the value is expressed in iso 4217
        alphabetical format (e.g. 'usd').
        :return: str
        """
        return self._get_parameter("payoutCcy")

    @payout_ccy.setter
    def payout_ccy(self, value):
        self._set_parameter("payoutCcy", value)

    @property
    def trigger_down(self):
        """
        The lower trigger of the binary option.
        :return: float
        """
        return self._get_parameter("triggerDown")

    @trigger_down.setter
    def trigger_down(self, value):
        self._set_parameter("triggerDown", value)

    @property
    def trigger_up(self):
        """
        The upper trigger of the binary option.
        :return: float
        """
        return self._get_parameter("triggerUp")

    @trigger_up.setter
    def trigger_up(self, value):
        self._set_parameter("triggerUp", value)
