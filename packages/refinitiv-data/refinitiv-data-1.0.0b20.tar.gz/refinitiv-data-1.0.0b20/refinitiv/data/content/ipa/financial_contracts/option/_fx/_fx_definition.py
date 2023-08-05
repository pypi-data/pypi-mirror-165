# coding: utf8

from typing import Optional, List

from .._base import UnderlyingDefinition
from ..._instrument_definition import InstrumentDefinition
from .._enums import (
    BuySell,
    CallPut,
    ExerciseStyle,
    UnderlyingType,
    SettlementType,
)
from . import (
    FxDualCurrencyDefinition,
    FxAverageInfo,
    FxBarrierDefinition,
    FxBinaryDefinition,
    FxDoubleBarrierDefinition,
    FxDoubleBinaryDefinition,
    FxForwardStart,
    FxUnderlyingDefinition,
)
from .._models import InputFlow


class FxDefinition(InstrumentDefinition):
    """
    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.it can be used to link output
        results to the instrument definition. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    start_date : str, optional
        Start date of the option
    end_date : str, optional
        The maturity or expiry date of the instrument. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z').
        optional. mandatory for otc eti options and fx options(if tenor is not defined).
        if instrumentcode of listed eti option is defined, the value comes from the
        instrument reference data.
    tenor : str, optional
        The code indicating the period between startdate and enddate of the instrument
        (e.g. '6m', '1y')
    notional_ccy : str, optional
        The currency of the instrument's notional amount. the value is expressed in iso
        4217 alphabetical format (e.g. 'usd'). if the option is a eurgbp call option,
        notionalccy can be expressed in eur or gbp mandatory for fx options.
    notional_amount : float, optional
        The notional amount of the instrument. if the option is a eurgbp call option,
        amount of eur or gbp of the contract
    asian_definition : FxOptionAverageInfo, optional

    barrier_definition : FxOptionBarrierDefinition, optional

    binary_definition : FxOptionBinaryDefinition, optional

    buy_sell : BuySell, optional
        The indicator of the deal side. the possible values are:
        - buy: buying the option,
        - sell: selling/writing the option. the output amounts calculated with taking
          buysell into consideration are returned with a reversed sign when the value
          'sell' is used. optional. the default value is 'buy'.
    call_put : CallPut, optional
        The indicator if the option is a call or a put. the possible values are:
        - call: the right to buy the underlying asset,
        - put: the right to sell the underlying asset. optional. if instrumentcode of
          listed eti option is defined, the value comes from the instrument reference
          data.the default value is 'call' for otc eti options and fx options.
    double_barrier_definition : FxOptionDoubleBarrierDefinition, optional

    double_binary_definition : FxOptionDoubleBinaryDefinition, optional

    dual_currency_definition : FxDualCurrencyDefinition, optional

    exercise_style : ExerciseStyle, optional
        The option style based on its exercise restrictions. the possible values are:
        - amer: the owner has the right to exercise on any date before the option
          expires,
        - euro: the owner has the right to exercise only on enddate,
        - berm: the owner has the right to exercise on any of several specified dates
          before the option expires. all exercise styles may not apply to certain option
          types. optional. if instrumentcode of listed eti option is defined, the value
          comes from the instrument reference data. the default value is 'euro' for otc
          eti options and fx options.
    forward_start_definition : FxOptionForwardStart, optional

    payments : InputFlow, optional
        An array of payments
    settlement_type : SettlementType, optional
        The settlement method for options when exercised. the possible values are:
        - physical(asset): delivering the underlying asset.
        - cash: paying out in cash.
    underlying_definition : FxUnderlyingDefinition, optional

    underlying_type : UnderlyingType, optional
        The type of the option based on the underlying asset. the possible values are:
        - eti: eti(exchanged traded instruments) options,
        - fx: fx options. mandatory. no default value applies.
    delivery_date : str, optional
        The date when the underlylng asset is delivered. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. '2021-01-01t00:00:00z').
    settlement_ccy : str, optional
        The currency of the instrument's settlement. the value is expressed in iso 4217
        alphabetical format (e.g. 'usd'). if the option is a eurgbp call option,
        settlementccy can be expressed in eur or gbp
    strike : float, optional
        The set price at which the owner of the option can buy or sell the underlying
        asset. the value is expressed according to the market convention linked to the
        underlying asset. optional. mandatory for otc eti options and fx options. if
        instrumentcode of listed eti option is defined, the value comes from the
        instrument reference data.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        asian_definition: Optional[FxAverageInfo] = None,
        barrier_definition: Optional[FxBarrierDefinition] = None,
        binary_definition: Optional[FxBinaryDefinition] = None,
        buy_sell: Optional[BuySell] = None,
        call_put: Optional[CallPut] = None,
        double_barrier_definition: Optional[FxDoubleBarrierDefinition] = None,
        double_binary_definition: Optional[FxDoubleBinaryDefinition] = None,
        dual_currency_definition: Optional[FxDualCurrencyDefinition] = None,
        exercise_style: Optional[ExerciseStyle] = None,
        forward_start_definition: Optional[FxForwardStart] = None,
        payments: Optional[List[InputFlow]] = None,
        settlement_type: Optional[SettlementType] = None,
        underlying_definition: Optional[FxUnderlyingDefinition] = None,
        underlying_type: Optional[UnderlyingType] = None,
        delivery_date: Optional[str] = None,
        settlement_ccy: Optional[str] = None,
        strike: Optional[float] = None,
        **kwargs,
    ) -> None:
        super().__init__(instrument_tag, **kwargs)
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.asian_definition = asian_definition
        self.barrier_definition = barrier_definition
        self.binary_definition = binary_definition
        self.buy_sell = buy_sell
        self.call_put = call_put
        self.double_barrier_definition = double_barrier_definition
        self.double_binary_definition = double_binary_definition
        self.dual_currency_definition = dual_currency_definition
        self.exercise_style = exercise_style
        self.forward_start_definition = forward_start_definition
        self.payments = payments
        self.settlement_type = settlement_type
        self.underlying_definition = underlying_definition
        self.underlying_type = underlying_type
        self.delivery_date = delivery_date
        self.settlement_ccy = settlement_ccy
        self.strike = strike

    @property
    def asian_definition(self):
        """
        :return: object FxOptionAverageInfo
        """
        return self._get_object_parameter(FxAverageInfo, "asianDefinition")

    @asian_definition.setter
    def asian_definition(self, value):
        self._set_object_parameter(FxAverageInfo, "asianDefinition", value)

    @property
    def barrier_definition(self):
        """
        :return: object FxOptionBarrierDefinition
        """
        return self._get_object_parameter(FxBarrierDefinition, "barrierDefinition")

    @barrier_definition.setter
    def barrier_definition(self, value):
        self._set_object_parameter(FxBarrierDefinition, "barrierDefinition", value)

    @property
    def binary_definition(self):
        """
        :return: object FxOptionBinaryDefinition
        """
        return self._get_object_parameter(FxBinaryDefinition, "binaryDefinition")

    @binary_definition.setter
    def binary_definition(self, value):
        self._set_object_parameter(FxBinaryDefinition, "binaryDefinition", value)

    @property
    def buy_sell(self):
        """
        The indicator of the deal side. the possible values are:
        - buy: buying the option,
        - sell: selling/writing the option. the output amounts calculated with taking
          buysell into consideration are returned with a reversed sign when the value
          'sell' is used. optional. the default value is 'buy'.
        :return: enum BuySell
        """
        return self._get_enum_parameter(BuySell, "buySell")

    @buy_sell.setter
    def buy_sell(self, value):
        self._set_enum_parameter(BuySell, "buySell", value)

    @property
    def call_put(self):
        """
        The indicator if the option is a call or a put. the possible values are:
        - call: the right to buy the underlying asset,
        - put: the right to sell the underlying asset. optional. if instrumentcode of
          listed eti option is defined, the value comes from the instrument reference
          data.the default value is 'call' for otc eti options and fx options.
        :return: enum CallPut
        """
        return self._get_enum_parameter(CallPut, "callPut")

    @call_put.setter
    def call_put(self, value):
        self._set_enum_parameter(CallPut, "callPut", value)

    @property
    def double_barrier_definition(self):
        """
        :return: object FxOptionDoubleBarrierDefinition
        """
        return self._get_object_parameter(
            FxDoubleBarrierDefinition, "doubleBarrierDefinition"
        )

    @double_barrier_definition.setter
    def double_barrier_definition(self, value):
        self._set_object_parameter(
            FxDoubleBarrierDefinition, "doubleBarrierDefinition", value
        )

    @property
    def double_binary_definition(self):
        """
        :return: object FxOptionDoubleBinaryDefinition
        """
        return self._get_object_parameter(
            FxDoubleBinaryDefinition, "doubleBinaryDefinition"
        )

    @double_binary_definition.setter
    def double_binary_definition(self, value):
        self._set_object_parameter(
            FxDoubleBinaryDefinition, "doubleBinaryDefinition", value
        )

    @property
    def dual_currency_definition(self):
        """
        :return: object FxDualCurrencyDefinition
        """
        return self._get_object_parameter(
            FxDualCurrencyDefinition, "dualCurrencyDefinition"
        )

    @dual_currency_definition.setter
    def dual_currency_definition(self, value):
        self._set_object_parameter(
            FxDualCurrencyDefinition, "dualCurrencyDefinition", value
        )

    @property
    def exercise_style(self):
        """
        The option style based on its exercise restrictions. the possible values are:
        - amer: the owner has the right to exercise on any date before the option
          expires,
        - euro: the owner has the right to exercise only on enddate,
        - berm: the owner has the right to exercise on any of several specified dates
          before the option expires. all exercise styles may not apply to certain option
          types. optional. if instrumentcode of listed eti option is defined, the value
          comes from the instrument reference data. the default value is 'euro' for otc
          eti options and fx options.
        :return: enum ExerciseStyle
        """
        return self._get_enum_parameter(ExerciseStyle, "exerciseStyle")

    @exercise_style.setter
    def exercise_style(self, value):
        self._set_enum_parameter(ExerciseStyle, "exerciseStyle", value)

    @property
    def forward_start_definition(self):
        """
        :return: object FxOptionForwardStart
        """
        return self._get_object_parameter(FxForwardStart, "forwardStartDefinition")

    @forward_start_definition.setter
    def forward_start_definition(self, value):
        self._set_object_parameter(FxForwardStart, "forwardStartDefinition", value)

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
    def settlement_type(self):
        """
        The settlement method for options when exercised. the possible values are:
        - physical(asset): delivering the underlying asset.
        - cash: paying out in cash.
        :return: enum SettlementType
        """
        return self._get_enum_parameter(SettlementType, "settlementType")

    @settlement_type.setter
    def settlement_type(self, value):
        self._set_enum_parameter(SettlementType, "settlementType", value)

    @property
    def underlying_definition(self):
        """
        :return: object FxUnderlyingDefinition
        """
        return self._get_object_parameter(UnderlyingDefinition, "underlyingDefinition")

    @underlying_definition.setter
    def underlying_definition(self, value):
        self._set_object_parameter(UnderlyingDefinition, "underlyingDefinition", value)

    @property
    def underlying_type(self):
        """
        The type of the option based on the underlying asset. the possible values are:
        - eti: eti(exchanged traded instruments) options,
        - fx: fx options. mandatory. no default value applies.
        :return: enum UnderlyingType
        """
        return self._get_enum_parameter(UnderlyingType, "underlyingType")

    @underlying_type.setter
    def underlying_type(self, value):
        self._set_enum_parameter(UnderlyingType, "underlyingType", value)

    @property
    def delivery_date(self):
        """
        The date when the underlylng asset is delivered. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. '2021-01-01t00:00:00z').
        :return: str
        """
        return self._get_parameter("deliveryDate")

    @delivery_date.setter
    def delivery_date(self, value):
        self._set_parameter("deliveryDate", value)

    @property
    def end_date(self):
        """
        The maturity or expiry date of the instrument. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z').
        optional. mandatory for otc eti options and fx options(if tenor is not defined).
        if instrumentcode of listed eti option is defined, the value comes from the
        instrument reference data.
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_parameter("endDate", value)

    @property
    def instrument_tag(self):
        """
        User defined string to identify the instrument.it can be used to link output
        results to the instrument definition. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        self._set_parameter("instrumentTag", value)

    @property
    def notional_amount(self):
        """
        The notional amount of the instrument. if the option is a eurgbp call option,
        amount of eur or gbp of the contract
        :return: float
        """
        return self._get_parameter("notionalAmount")

    @notional_amount.setter
    def notional_amount(self, value):
        self._set_parameter("notionalAmount", value)

    @property
    def notional_ccy(self):
        """
        The currency of the instrument's notional amount. the value is expressed in iso
        4217 alphabetical format (e.g. 'usd'). if the option is a eurgbp call option,
        notionalccy can be expressed in eur or gbp mandatory for fx options.
        :return: str
        """
        return self._get_parameter("notionalCcy")

    @notional_ccy.setter
    def notional_ccy(self, value):
        self._set_parameter("notionalCcy", value)

    @property
    def settlement_ccy(self):
        """
        The currency of the instrument's settlement. the value is expressed in iso 4217
        alphabetical format (e.g. 'usd'). if the option is a eurgbp call option,
        settlementccy can be expressed in eur or gbp
        :return: str
        """
        return self._get_parameter("settlementCcy")

    @settlement_ccy.setter
    def settlement_ccy(self, value):
        self._set_parameter("settlementCcy", value)

    @property
    def start_date(self):
        """
        Start date of the option
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_parameter("startDate", value)

    @property
    def strike(self):
        """
        The set price at which the owner of the option can buy or sell the underlying
        asset. the value is expressed according to the market convention linked to the
        underlying asset. optional. mandatory for otc eti options and fx options. if
        instrumentcode of listed eti option is defined, the value comes from the
        instrument reference data.
        :return: float
        """
        return self._get_parameter("strike")

    @strike.setter
    def strike(self, value):
        self._set_parameter("strike", value)

    @property
    def tenor(self):
        """
        The code indicating the period between startdate and enddate of the instrument
        (e.g. '6m', '1y')
        :return: str
        """
        return self._get_parameter("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_parameter("tenor", value)
