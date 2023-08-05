# coding: utf8

from typing import Optional

from .._instrument_definition import InstrumentDefinition
from ._enums import (
    AdjustInterestToPaymentDate,
    BusinessDayConvention,
    BuySell,
    DateRollingConvention,
    DayCountBasis,
    Frequency,
    IndexResetType,
    InterestCalculationConvention,
    StubRule,
)
from ._models import (
    AmortizationItem,
    BarrierDefinitionElement,
    InputFlow,
)


class CapFloorInstrumentDefinition(InstrumentDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
    start_date : str, optional
        The option start date
    end_date : str, optional
        The maturity date of the CapFloor
    tenor : str, optional
        Tenor of the option
    notional_ccy : str, optional
        The ISO code of the notional currency. Mandatory if instrument code or
        instrument style has not been defined. In case an instrument code/style has been
        defined, value may comes from the reference data.
    notional_amount : float, optional
        The notional amount of the leg at the period start date. Optional. By default
        1,000,000 is used.
    index_name : str, optional
        The name of the floating rate index.
    index_tenor : str, optional
        The period code that represents the maturity of the floating rate index.
        Mandatory when the leg is float.
    interest_payment_frequency : Frequency, optional
        The frequency of the interest payments. Optional if an instrument code/style
        have been defined : in that case, value comes from reference data. Otherwise, it
        is mandatory.
    interest_calculation_method : DayCountBasis, optional
        The Day Count Basis method used to calculate the coupon interest payments.
        Mandatory.
    payment_business_day_convention : BusinessDayConvention, optional
        The method to adjust dates to a working day. The possible values are:
        - ModifiedFollowing (adjusts dates according to the Modified Following
          convention - next business day unless is it goes into the next month,
          preceeding is used in that  case),
        - NextBusinessDay (adjusts dates according to the Following convention - Next
          Business Day),
        - PreviousBusinessDay (adjusts dates  according to the Preceeding convention -
          Previous Business Day),
        - NoMoving (does not adjust dates),
        - BbswModifiedFollowing (adjusts dates  according to the BBSW Modified Following
          convention). Optional. In case an instrument code/style has been defined,
          value comes from bond reference data. Otherwise 'ModifiedFollowing' is used.
    payment_roll_convention : DateRollingConvention, optional
        The method to adjust payment dates whn they fall at the end of the month (28th
        of February, 30th, 31st). The possible values are:
        - Last (For setting the calculated date to the last working day),
        - Same (For setting the calculated date to the same day . In this latter case,
          the date may be moved according to the date moving convention if it is a
          non-working day),
        - Last28 (For setting the calculated date to the last working day. 28FEB being
          always considered as the last working day),
        - Same28 (For setting the calculated date to the same day .28FEB being always
          considered as the last working day). Optional. By default 'SameDay' is used.
    index_reset_frequency : Frequency, optional
        The reset frequency in case the leg Type is Float. Optional. By default the
        IndexTenor is used.
    index_reset_type : IndexResetType, optional
        A flag that indicates if the floating rate index is reset before the coupon
        period starts or at the end of the coupon period. The possible values are:
        - InAdvance (resets the index before the start of the interest period),
        - InArrears (resets the index at the end of the interest period). Optional. By
          default 'InAdvance' is used.
    index_fixing_lag : int, optional
        Defines the positive number of working days between the fixing date and the
        start of the coupon period ('InAdvance') or the end of the coupon period
        ('InArrears'). Optional. By default 0 is used.
    amortization_schedule : AmortizationItem, optional
        Definition of amortizations
    payment_business_days : str, optional
        A list of coma-separated calendar codes to adjust dates (e.g. 'EMU' or 'USA').
        Optional. By default the calendar associated to NotionalCcy is used.
    adjust_interest_to_payment_date : AdjustInterestToPaymentDate, optional
        A flag that indicates if the coupon dates are adjusted to the payment dates.
        Optional. By default 'false' is used.
    stub_rule : StubRule, optional
        The rule that defines whether coupon roll dates are aligned on the  maturity or
        the issue date. The possible values are:
        - ShortFirstProRata (to create a short period between the start date and the
          first coupon date, and pay a smaller amount of interest for the short
          period.All coupon dates are calculated backward from the maturity date),
        - ShortFirstFull (to create a short period between the start date and the first
          coupon date, and pay a regular coupon on the first coupon date. All coupon
          dates are calculated backward from the maturity date),
        - LongFirstFull (to create a long period between the start date and the second
          coupon date, and pay a regular coupon on the second coupon date. All coupon
          dates are calculated backward from the maturity date),
        - ShortLastProRata (to create a short period between the last payment date and
          maturity, and pay a smaller amount of interest for the short period. All
          coupon dates are calculated forward from the start date). This property may
          also be used in conjunction with firstRegularPaymentDate and
          lastRegularPaymentDate; in that case the following values can be defined:
        - Issue (all dates are aligned on the issue date),
        - Maturity (all dates are aligned on the maturity date). Optional. By default
          'Maturity' is used.
    barrier_definition : BarrierDefinitionElement, optional

    buy_sell : BuySell, optional
        The side of the deal. Possible values:
        - Buy
        - Sell
    annualized_rebate : bool, optional

    cap_digital_payout_percent : float, optional

    cap_strike_percent : float, optional
        Cap leg strike expressed in %
    cms_template : str, optional
        A reference to a common swap contract that represents the underlying swap in
        case of a Constant Maturity Swap contract (CMS). Mandatory for CMS contract.
    floor_digital_payout_percent : float, optional

    floor_strike_percent : float, optional
        Floor leg strike expressed in %
    index_fixing_ric : str, optional
        The RIC that carries the fixing value. This value overrides the RIC associated
        by default with the IndexName and IndexTenor. Optional.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        index_name: Optional[str] = None,
        index_tenor: Optional[str] = None,
        interest_payment_frequency: Optional[Frequency] = None,
        interest_calculation_method: Optional[DayCountBasis] = None,
        payment_business_day_convention: Optional[BusinessDayConvention] = None,
        payment_roll_convention: Optional[DateRollingConvention] = None,
        index_reset_frequency: Optional[Frequency] = None,
        index_reset_type: Optional[IndexResetType] = None,
        index_fixing_lag: Optional[int] = None,
        amortization_schedule: Optional[AmortizationItem] = None,
        payment_business_days: Optional[str] = None,
        adjust_interest_to_payment_date: Optional[AdjustInterestToPaymentDate] = None,
        stub_rule: Optional[StubRule] = None,
        barrier_definition: Optional[BarrierDefinitionElement] = None,
        buy_sell: Optional[BuySell] = None,
        interest_calculation_convention: Optional[InterestCalculationConvention] = None,
        payments: Optional[InputFlow] = None,
        annualized_rebate: Optional[bool] = None,
        cap_digital_payout_percent: Optional[float] = None,
        cap_strike_percent: Optional[float] = None,
        cms_template: Optional[str] = None,
        floor_digital_payout_percent: Optional[float] = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        is_backward_looking_index: Optional[bool] = None,
        is_rfr: Optional[bool] = None,
        is_term_rate: Optional[bool] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_reset_type = index_reset_type
        self.index_fixing_lag = index_fixing_lag
        self.amortization_schedule = amortization_schedule
        self.payment_business_days = payment_business_days
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.stub_rule = stub_rule
        self.barrier_definition = barrier_definition
        self.buy_sell = buy_sell
        self.interest_calculation_convention = interest_calculation_convention
        self.payments = payments
        self.annualized_rebate = annualized_rebate
        self.cap_digital_payout_percent = cap_digital_payout_percent
        self.cap_strike_percent = cap_strike_percent
        self.cms_template = cms_template
        self.floor_digital_payout_percent = floor_digital_payout_percent
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.is_backward_looking_index = is_backward_looking_index
        self.is_rfr = is_rfr
        self.is_term_rate = is_term_rate

    @classmethod
    def get_instrument_type(cls):
        return "CapFloor"

    @property
    def adjust_interest_to_payment_date(self):
        """
        An indication if the coupon dates are adjusted to the payment dates. the
        possible values are:    adjusted,    unadjusted.  optional. the default value is
        'unadjusted'.
        :return: enum AdjustInterestToPaymentDate
        """
        return self._get_enum_parameter(
            AdjustInterestToPaymentDate, "adjustInterestToPaymentDate"
        )

    @adjust_interest_to_payment_date.setter
    def adjust_interest_to_payment_date(self, value):
        self._set_enum_parameter(
            AdjustInterestToPaymentDate, "adjustInterestToPaymentDate", value
        )

    @property
    def amortization_schedule(self):
        """
        The amortization schedule of the instrument. it contains the following
        information:      startdate,      enddate,      remainingnotional,
        amortizationfrequency,      amount,      amortizationtype.   no default value
        applies.
        :return: list AmortizationItem
        """
        return self._get_list_parameter(AmortizationItem, "amortizationSchedule")

    @amortization_schedule.setter
    def amortization_schedule(self, value):
        self._set_list_parameter(AmortizationItem, "amortizationSchedule", value)

    @property
    def barrier_definition(self):
        """
        :return: object BarrierDefinitionElement
        """
        return self._get_object_parameter(BarrierDefinitionElement, "barrierDefinition")

    @barrier_definition.setter
    def barrier_definition(self, value):
        self._set_object_parameter(BarrierDefinitionElement, "barrierDefinition", value)

    @property
    def buy_sell(self):
        """
        The indicator of the deal side. the possible values are:   buy: buying the
        option,   sell: selling/writing the option.  mandatory. no default value
        applies.
        :return: enum BuySell
        """
        return self._get_enum_parameter(BuySell, "buySell")

    @buy_sell.setter
    def buy_sell(self, value):
        self._set_enum_parameter(BuySell, "buySell", value)

    @property
    def index_reset_frequency(self):
        """
        The reset frequency for the floating instrument. optional. by default, the reset
        frequency associated to  the index defined for the floating leg is used.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "indexResetFrequency")

    @index_reset_frequency.setter
    def index_reset_frequency(self, value):
        self._set_enum_parameter(Frequency, "indexResetFrequency", value)

    @property
    def index_reset_type(self):
        """
        A flag that indicates if the floating rate index is reset before the coupon
        period starts or at the end of the coupon period. the possible values are:
        inadvance (resets the index before the start of the interest period),
        inarrears (resets the index at the end of the interest period).  optional. the
        default value is 'inadvance'.
        :return: enum IndexResetType
        """
        return self._get_enum_parameter(IndexResetType, "indexResetType")

    @index_reset_type.setter
    def index_reset_type(self, value):
        self._set_enum_parameter(IndexResetType, "indexResetType", value)

    @property
    def interest_calculation_convention(self):
        """
        The day count basis method convention used to calculate the interest payments.
        optional. defaults to moneymarket.
        :return: enum InterestCalculationConvention
        """
        return self._get_enum_parameter(
            InterestCalculationConvention, "interestCalculationConvention"
        )

    @interest_calculation_convention.setter
    def interest_calculation_convention(self, value):
        self._set_enum_parameter(
            InterestCalculationConvention, "interestCalculationConvention", value
        )

    @property
    def interest_calculation_method(self):
        """
        The interest payment frequency (e.g : annual, semiannual, quartely). the default
        value is selected based onnotionalccy.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "interestCalculationMethod")

    @interest_calculation_method.setter
    def interest_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "interestCalculationMethod", value)

    @property
    def interest_payment_frequency(self):
        """
        The interest payment frequency. by default, indextenor is used, if it is
        defined. otherwise, the default value is indexresetfrequency.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "interestPaymentFrequency")

    @interest_payment_frequency.setter
    def interest_payment_frequency(self, value):
        self._set_enum_parameter(Frequency, "interestPaymentFrequency", value)

    @property
    def payment_business_day_convention(self):
        """
        The method to adjust dates to working days. the possible values are:
        previousbusinessday,    nextbusinessday,    modified following,    nomoving,
        bswmodifiedfollowing.  optional. if instrumentcode is defined, the value comes
        from the instrument reference data. in case of a user-defined instrument, the
        default value is'modifiedfollowing'.
        :return: enum BusinessDayConvention
        """
        return self._get_enum_parameter(
            BusinessDayConvention, "paymentBusinessDayConvention"
        )

    @payment_business_day_convention.setter
    def payment_business_day_convention(self, value):
        self._set_enum_parameter(
            BusinessDayConvention, "paymentBusinessDayConvention", value
        )

    @property
    def payment_roll_convention(self):
        """
        The method to adjust payment dates when they fall at the end of the month (e.g.
        28th of february, 30th, 31st). the possible values are:    last,    same,
        last28,    same28.  optional. if instrumentcode is defined, the value comes from
        the instrument reference data. in case of a user-defined instrument, the default
        value is'last'.
        :return: enum DateRollingConvention
        """
        return self._get_enum_parameter(DateRollingConvention, "paymentRollConvention")

    @payment_roll_convention.setter
    def payment_roll_convention(self, value):
        self._set_enum_parameter(DateRollingConvention, "paymentRollConvention", value)

    @property
    def payments(self):
        """
        An array of historical payments
        :return: list InputFlow
        """
        return self._get_list_parameter(InputFlow, "payments")

    @payments.setter
    def payments(self, value):
        self._set_list_parameter(InputFlow, "payments", value)

    @property
    def stub_rule(self):
        """
        The rule that defines whether coupon roll dates are aligned to the maturity or
        issue date. the possible values are:    issue,    maturity,
        shortfirstprorata,    shortfirstfull,    longfirstfull,    shortlastprorata.
        optional. the default value is 'maturity'.
        :return: enum StubRule
        """
        return self._get_enum_parameter(StubRule, "stubRule")

    @stub_rule.setter
    def stub_rule(self, value):
        self._set_enum_parameter(StubRule, "stubRule", value)

    @property
    def annualized_rebate(self):
        """
        An indicator if the rebate is adjusted according to the frequency of the cap.
        for example, if the frequency of the cap is quarterly (frq:4), all rebates are
        divided by four (approximately). the possible values are:   true: the rebates
        are adjusted,   false: there is no rebate adjustment(the rebate value is assumed
        to be annualized).  the default value is 'false'.
        :return: bool
        """
        return self._get_parameter("annualizedRebate")

    @annualized_rebate.setter
    def annualized_rebate(self, value):
        self._set_parameter("annualizedRebate", value)

    @property
    def cap_digital_payout_percent(self):
        """
        A percentage of notionalamount that is received (paid) by the option buyer
        (seller) if the option expires on or above the cap strike. no default value
        applies.
        :return: float
        """
        return self._get_parameter("capDigitalPayoutPercent")

    @cap_digital_payout_percent.setter
    def cap_digital_payout_percent(self, value):
        self._set_parameter("capDigitalPayoutPercent", value)

    @property
    def cap_strike_percent(self):
        """
        The contractual strike rate of the cap. the value is expressed in percentages.
        either capstrikepercent or capstrikepercentschedule must be provided. no default
        value applies.
        :return: float
        """
        return self._get_parameter("capStrikePercent")

    @cap_strike_percent.setter
    def cap_strike_percent(self, value):
        self._set_parameter("capStrikePercent", value)

    @property
    def cms_template(self):
        """
        A reference to a common swap contract that represents the underlying swap in
        case of a constant maturity swap contract (cms). example: eur_ab6e. no default
        value applies.
        :return: str
        """
        return self._get_parameter("cmsTemplate")

    @cms_template.setter
    def cms_template(self, value):
        self._set_parameter("cmsTemplate", value)

    @property
    def end_date(self):
        """
        The maturity or expiry date of the instrument. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z). either
        tenor or enddate must be provided. the default value is valuationdate shifted
        forward by tenor.
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_parameter("endDate", value)

    @property
    def floor_digital_payout_percent(self):
        """
        A percentage of notionalamount that is received (paid) by the option buyer
        (seller) if the option expires on or below the floor strike. no default value
        applies.
        :return: float
        """
        return self._get_parameter("floorDigitalPayoutPercent")

    @floor_digital_payout_percent.setter
    def floor_digital_payout_percent(self, value):
        self._set_parameter("floorDigitalPayoutPercent", value)

    @property
    def floor_strike_percent(self):
        """
        The contractual strike rate of the floor. the value is expressed in percentages.
        either floorstrikepercent or floorstrikepercentschedule must be provided. no
        default value applies.
        :return: float
        """
        return self._get_parameter("floorStrikePercent")

    @floor_strike_percent.setter
    def floor_strike_percent(self, value):
        self._set_parameter("floorStrikePercent", value)

    @property
    def index_fixing_lag(self):
        """
        The number of working days between the fixing date of the index and the start of
        the coupon period ('inadvance') or the end of the coupon period ('inarrears').
        optional. if indexfixingric or indexname is defined, the associated fixing lag
        is selected. otherwise, the value is based on the first fixing that matches
        currency and indextenor.
        :return: int
        """
        return self._get_parameter("indexFixingLag")

    @index_fixing_lag.setter
    def index_fixing_lag(self, value):
        self._set_parameter("indexFixingLag", value)

    @property
    def index_fixing_ric(self):
        """
        The ric that carries the fixing value if the instrument has a floating interest.
        optional. no default value applies.
        :return: str
        """
        return self._get_parameter("indexFixingRic")

    @index_fixing_ric.setter
    def index_fixing_ric(self, value):
        self._set_parameter("indexFixingRic", value)

    @property
    def index_name(self):
        """
        The name of the floating rate index (e.g. 'euribor'). optional. no default value
        applies.
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)

    @property
    def index_tenor(self):
        """
        The period code indicating the maturity of the floating rate index. if
        indexfixingric is defined, the values comes from the instrument reference data.
        otherwise, the default value is the tenor equivalent toindexresetfrequency or
        interestpaymentfrequency.
        :return: str
        """
        return self._get_parameter("indexTenor")

    @index_tenor.setter
    def index_tenor(self, value):
        self._set_parameter("indexTenor", value)

    @property
    def instrument_tag(self):
        """
        A user defined string to identify the instrument. it can be used to link output
        results to the instrument definition.limited to 40 characters. only alphabetic,
        numeric and '- _.#=@' characters are supported. optional. no default value
        applies.
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        self._set_parameter("instrumentTag", value)

    @property
    def is_backward_looking_index(self):
        """
        An indicator if the underlying fixing rate is backward-looking (mostly
        risk-free-rate). the possible values are: false: the underlying fixing rate is
        forward-looking and the rate of each caplet is fixed at the start of the caplet
        period. true: the underlying fixing rate is backward-looking. for backward
        looking caps/floors the rate is accreted up to the end of the caplet period.
        :return: bool
        """
        return self._get_parameter("isBackwardLookingIndex")

    @is_backward_looking_index.setter
    def is_backward_looking_index(self, value):
        self._set_parameter("isBackwardLookingIndex", value)

    @property
    def is_rfr(self):
        """
        :return: bool
        """
        return self._get_parameter("isRfr")

    @is_rfr.setter
    def is_rfr(self, value):
        self._set_parameter("isRfr", value)

    @property
    def is_term_rate(self):
        """
        :return: bool
        """
        return self._get_parameter("isTermRate")

    @is_term_rate.setter
    def is_term_rate(self, value):
        self._set_parameter("isTermRate", value)

    @property
    def notional_amount(self):
        """
        The notional amount of the instrument. optional. the default value is
        '1,000,000' in notionalccy.
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
        4217 alphabetical format (e.g. 'usd'). no default value applies. mandatory if
        instrument code or instrument style has not been defined. in case an instrument
        code/style has been defined, value may comes from the reference data.
        :return: str
        """
        return self._get_parameter("notionalCcy")

    @notional_ccy.setter
    def notional_ccy(self, value):
        self._set_parameter("notionalCcy", value)

    @property
    def payment_business_days(self):
        """
        A list of comma-separated calendar codes to adjust dates (e.g. 'emu' or 'usa').
        no default value applies.
        :return: str
        """
        return self._get_parameter("paymentBusinessDays")

    @payment_business_days.setter
    def payment_business_days(self, value):
        self._set_parameter("paymentBusinessDays", value)

    @property
    def start_date(self):
        """
        The start date of the instrument. this value is expressed in iso 8601 format:
        yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z). the default value is
        valuationdate shifted forward by a month using market conventions.
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_parameter("startDate", value)

    @property
    def tenor(self):
        """
        The code indicating the tenor of the instrument (e.g. '5m'). mandatory if
        enddate is not provided. no default value applies.
        :return: str
        """
        return self._get_parameter("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_parameter("tenor", value)
