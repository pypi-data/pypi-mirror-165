# coding: utf8


from typing import Optional, List

from . import BermudanSwaptionDefinition
from ._enums import (
    BuySell,
    ExerciseStyle,
    PremiumSettlementType,
    SwaptionSettlementType,
    SwaptionType,
)
from ._models import InputFlow
from .. import swap
from .._instrument_definition import InstrumentDefinition
from ..swap._swap_definition import SwapInstrumentDefinition


class SwaptionInstrumentDefinition(InstrumentDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        A user defined string to identify the instrument. it can be used to link output
        results to the instrument definition.limited to 40 characters.only alphabetic,
        numeric and '- _.#=@' characters are supported. optional. no default value
        applies.
    start_date : str, optional
        The date the swaption starts. optional. by default it is derived from the
        tradedate and the day to spot convention of the contract currency.
    end_date : str, optional
        The maturity or expiry date of the instrument's leg. the value is expressed in
        iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z). either
        tenor or enddate must be provided. the default value is valuationdate shifted
        forward by tenor.
    tenor : str, optional
        The code indicating the period between startdate and enddate of the instrument
        (e.g. '6m', '1y'). mandatory, if enddate is not provided. the default value is
        calculated from enddate.
    notional_amount : float, optional
        The notional amount of the instrument. the default value is '1,000,000'.
    bermudan_swaption_definition : BermudanSwaptionDefinition, optional

    buy_sell : BuySell, optional
        The indicator of the deal side. the possible values are:   buy: buying the
        option,   sell: selling/writing the option.  no default value applies.
    exercise_style : ExerciseStyle, optional
        The option style based on its exercise restrictions. the possible values are:
        amer,   euro,   berm.  note: all exercise styles may not apply to certain option
        no default value applies.
    payments : InputFlow, optional
        An array of payments
    premium_settlement_type : PremiumSettlementType, optional
        The cash settlement type of the option premium   spot,   forward.
    settlement_type : SwaptionSettlementType, optional
        The settlement method for options when exercised. the possible values are:
        physical: delivering the underlying asset, or for a swaption, physically
        entering into the underlying swap.    cash: paying out in cash.  the default
        value is 'physical'.
    swaption_type : SwaptionType, optional
        The indicator if the swaption is a payer or a receiver. the possible values are:
        receiver: a right to receive a fixed rate of the underlying swap,   payer: a
        right to pay a fixed rate of the underlying swap.  no default value applies.
    underlying_definition : SwapDefinition, optional

    spread_vs_atm_in_bp : float, optional
        Spread between strike and atm strike, expressed in basis points (bp).
    strike_percent : float, optional
        The set price at which the owner of the option can buy or sell the underlying
        asset. for a swaption, it is the fixed rate of the underlying swap at which the
        owner of the swaption can enter the swap. the value is expressed in percentages.
        by default, fixedratepercent of the underlying swap is used.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        notional_amount: Optional[float] = None,
        bermudan_swaption_definition: Optional[BermudanSwaptionDefinition] = None,
        buy_sell: Optional[BuySell] = None,
        exercise_style: Optional[ExerciseStyle] = None,
        payments: Optional[List[InputFlow]] = None,
        premium_settlement_type: Optional[PremiumSettlementType] = None,
        settlement_type: Optional[SwaptionSettlementType] = None,
        swaption_type: Optional[SwaptionType] = None,
        underlying_definition: Optional[swap.Definition] = None,
        spread_vs_atm_in_bp: Optional[float] = None,
        strike_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_amount = notional_amount
        self.bermudan_swaption_definition = bermudan_swaption_definition
        self.buy_sell = buy_sell
        self.exercise_style = exercise_style
        self.payments = payments
        self.premium_settlement_type = premium_settlement_type
        self.settlement_type = settlement_type
        self.swaption_type = swaption_type
        self.underlying_definition = underlying_definition
        self.spread_vs_atm_in_bp = spread_vs_atm_in_bp
        self.strike_percent = strike_percent

    @classmethod
    def get_instrument_type(cls):
        return "Swaption"

    @property
    def bermudan_swaption_definition(self):
        """
        :return: object BermudanSwaptionDefinition
        """
        return self._get_object_parameter(
            BermudanSwaptionDefinition, "bermudanSwaptionDefinition"
        )

    @bermudan_swaption_definition.setter
    def bermudan_swaption_definition(self, value):
        self._set_object_parameter(
            BermudanSwaptionDefinition, "bermudanSwaptionDefinition", value
        )

    @property
    def buy_sell(self):
        """
        The side of the deal.
        :return: enum BuySell
        """
        return self._get_enum_parameter(BuySell, "buySell")

    @buy_sell.setter
    def buy_sell(self, value):
        self._set_enum_parameter(BuySell, "buySell", value)

    @property
    def exercise_style(self):
        """
        :return: enum ExerciseStyle
        """
        return self._get_enum_parameter(ExerciseStyle, "exerciseStyle")

    @exercise_style.setter
    def exercise_style(self, value):
        self._set_enum_parameter(ExerciseStyle, "exerciseStyle", value)

    @property
    def payments(self):
        """
        An array of payments
        :return: list InputFlow
        """
        return self._get_list_parameter(InputFlow, "payments")

    @payments.setter
    def payments(self, value):
        self._set_list_parameter(InputFlow, "payments", value)

    @property
    def premium_settlement_type(self):
        """
        The cash settlement type of the option premium   spot,   forward.
        :return: enum PremiumSettlementType
        """
        return self._get_enum_parameter(PremiumSettlementType, "premiumSettlementType")

    @premium_settlement_type.setter
    def premium_settlement_type(self, value):
        self._set_enum_parameter(PremiumSettlementType, "premiumSettlementType", value)

    @property
    def settlement_type(self):
        """
        The settlement type of the option if the option is exercised.
        :return: enum SwaptionSettlementType
        """
        return self._get_enum_parameter(SwaptionSettlementType, "settlementType")

    @settlement_type.setter
    def settlement_type(self, value):
        self._set_enum_parameter(SwaptionSettlementType, "settlementType", value)

    @property
    def swaption_type(self):
        """
        The indicator if the swaption is a payer or a receiver. the possible values are:
        receiver: a right to receive a fixed rate of the underlying swap,   payer: a
        right to pay a fixed rate of the underlying swap.  no default value applies.
        :return: enum SwaptionType
        """
        return self._get_enum_parameter(SwaptionType, "swaptionType")

    @swaption_type.setter
    def swaption_type(self, value):
        self._set_enum_parameter(SwaptionType, "swaptionType", value)

    @property
    def underlying_definition(self):
        """
        :return: object SwapDefinition
        """
        return self._get_object_parameter(
            SwapInstrumentDefinition, "underlyingDefinition"
        )

    @underlying_definition.setter
    def underlying_definition(self, value):
        self._set_object_parameter(
            SwapInstrumentDefinition, "underlyingDefinition", value
        )

    @property
    def end_date(self):
        """
        The maturity or expiry date of the instrument's leg. the value is expressed in
        iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z). either
        tenor or enddate must be provided. the default value is valuationdate shifted
        forward by tenor.
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_parameter("endDate", value)

    @property
    def instrument_tag(self):
        """
        A user defined string to identify the instrument. it can be used to link output
        results to the instrument definition.limited to 40 characters.only alphabetic,
        numeric and '- _.#=@' characters are supported. optional. no default value
        applies.
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        self._set_parameter("instrumentTag", value)

    @property
    def notional_amount(self):
        """
        The notional amount of the instrument. The default value is '1,000,000'.
        :return: float
        """
        return self._get_parameter("notionalAmount")

    @notional_amount.setter
    def notional_amount(self, value):
        self._set_parameter("notionalAmount", value)

    @property
    def spread_vs_atm_in_bp(self):
        """
        Spread between strike and atm strike, expressed in basis points (bp).
        :return: float
        """
        return self._get_parameter("spreadVsAtmInBp")

    @spread_vs_atm_in_bp.setter
    def spread_vs_atm_in_bp(self, value):
        self._set_parameter("spreadVsAtmInBp", value)

    @property
    def start_date(self):
        """
        The date the swaption starts. optional. by default it is derived from the
        tradedate and the day to spot convention of the contract currency.
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_parameter("startDate", value)

    @property
    def strike_percent(self):
        """
        The set price at which the owner of the option can buy or sell the underlying
        asset. for a swaption, it is the fixed rate of the underlying swap at which the
        owner of the swaption can enter the swap. the value is expressed in percentages.
        by default, fixedratepercent of the underlying swap is used.
        :return: float
        """
        return self._get_parameter("strikePercent")

    @strike_percent.setter
    def strike_percent(self, value):
        self._set_parameter("strikePercent", value)

    @property
    def tenor(self):
        """
        The code indicating the period between startdate and enddate of the instrument
        (e.g. '6m', '1y'). mandatory, if enddate is not provided. the default value is
        calculated from enddate.
        :return: str
        """
        return self._get_parameter("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_parameter("tenor", value)
