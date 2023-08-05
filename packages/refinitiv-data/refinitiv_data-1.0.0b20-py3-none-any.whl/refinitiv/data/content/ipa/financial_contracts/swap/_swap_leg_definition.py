# coding: utf8


from typing import Optional, List

from ._enums import (
    AdjustInterestToPaymentDate,
    BusinessDayConvention,
    DateRollingConvention,
    DayCountBasis,
    Direction,
    Frequency,
    IndexAverageMethod,
    IndexCompoundingMethod,
    IndexObservationMethod,
    IndexResetType,
    IndexSpreadCompoundingMethod,
    InterestCalculationConvention,
    InterestType,
    NotionalExchange,
    StubRule,
)
from ._models import AmortizationItem
from ..._object_definition import ObjectDefinition


class LegDefinition(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional

    leg_tag : str, optional
        A user-defined string to identify the direction of the leg: 'paid' or
        'received'. optional. no default value applies.
    direction : Direction, optional
        The indication whether the cash flows of the instrument's leg are paid or
        received. the possible values are:   paid: the cash flows are paid to the
        counterparty,   received: the cash flows are received from the counterparty.  no
        default value applies.
    interest_type : InterestType, optional
        An indicator whether the instrument pays a fixed or floating interest. the
        possible values are: fixed, float. no default value applies.
    notional_ccy : str, optional
        The currency of the instrument's notional amount. the value is expressed in iso
        4217 alphabetical format (e.g. 'usd'). no default value applies.
    notional_amount : float, optional
        The notional amount of the instrument's leg. the default value is '1,000,000'.
    fixed_rate_percent : float, optional
        The interest rate of the instrument. the value is expressed in percentages.
        mandatory if no instrumentcode is defined. if instrumentcode is defined, the
        value comes from the instrument reference data.
    index_name : str, optional
        The name of the floating rate index (e.g. 'euribor'). no default value applies.
    index_tenor : str, optional
        The period code indicating the maturity of the floating rate index. the default
        value is the tenor equivalent toindexresetfrequency or interestpaymentfrequency.
    spread_bp : float, optional
        The interest spread in basis points that is added to the floating rate index
        value. optional. if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is '0'.
    interest_payment_frequency : Frequency, optional
        The frequency of the interest payment. either indexresetfrequency or
        interestpaymentfrequency must be provided (e.g. annual, semiannual).   the
        default value is indexresetfrequency.
    interest_calculation_method : DayCountBasis, optional
        The day count basis method used to calculate the interest payments(e.g.
        dcb_30_360, dcb_30_actual). the default value is selected based onnotionalccy.
    accrued_calculation_method : DayCountBasis, optional
        The day count basis method used to calculate the accrued interest payments (e.g.
        dcb_30_360, dcb_30_actual).   if instrumentcode is defined, the value comes from
        the instrument reference data. in case of a user-defined instrument,
        interestcalculationmethod is used.
    payment_business_day_convention : BusinessDayConvention, optional
        The method to adjust dates to working days. the possible values are:
        previousbusinessday,    nextbusinessday,    modified following,    nomoving,
        bbswmodifiedfollowing.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'modifiedfollowing'.
    payment_roll_convention : DateRollingConvention, optional
        The method to adjust payment dates when they fall at the end of the month (e.g.
        28th of february, 30th, 31st). the possible values are:    last,    same,
        last28,    same28.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'same'.
    index_reset_frequency : Frequency, optional
        The reset frequency for the floating instrument (e.g. annual, semiannual).   the
        default value is interestpaymentfrequency.
    index_reset_type : IndexResetType, optional
        A type indicating if the floating rate index is reset before the coupon period
        starts or at the end of the coupon period. the possible values are: inadvance:
        resets the index before the start of the interest period, inarrears: resets the
        index at the end of the interest period. the default value is 'inadvance'.
    index_fixing_lag : int, optional
        The number of working daysbetween the fixing date and the start of the coupon
        period ('inadvance') or the end of the coupon period ('inarrears'). the
        inadvance/inarrears mode is set in the indexresettype parameter. the default
        value is the fixing lag associated to the index defined/determined by default on
        the floating instrument.
    first_regular_payment_date : str, optional
        The first regular interest payment date used for the odd first interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
    last_regular_payment_date : str, optional
        The last regular interest payment date used for the odd last interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
    amortization_schedule : AmortizationItem, optional
        The amortization schedule of the instrument. it contains the following
        information:   startdate,   enddate,   remainingnotional,
        amortizationfrequency,   amount,   amortizationtype.  optional. no default value
        applies.
    payment_business_days : str, optional
        A list of comma-separated calendar codes to adjust dates (e.g. 'emu' or 'usa').
        the default value is the calendar associated to the market conventions of the
        interestpaymentccy for the corresponding leg.
    notional_exchange : NotionalExchange, optional
        An indicator if the notional amount is exchanged and when it is exchanged. the
        possible values are:    none,    start,    end,    both,    endadjustment.   the
        default value is 'none'.
    adjust_interest_to_payment_date : AdjustInterestToPaymentDate, optional
        An indication if the coupon dates are adjusted to the payment dates. the
        possible values are:   adjusted,   unadjusted.  if instrumentcode is defined,
        the value comes from the instrument reference data. in case of a user-defined
        instrument, the default value is 'adjusted'.
    index_compounding_method : IndexCompoundingMethod, optional
        The method how the interest rate is calculated from the reset floating rates
        when the reset frequency is higher than the interest payment frequency (e.g.
        daily index reset with quarterly interest payments). the possible values are:
        compounded, average, constant, adjustedcompounded, mexicancompounded. if
        instrumentcode is defined, the value comes from the instrument reference data.
        in case of a user-defined instrument, the default value is 'constant'.
    interest_payment_delay : int, optional
        The number of working days between the end of the interest accrual period and
        the interest payment date. by default, no delay (0) is applied.
    stub_rule : StubRule, optional
        The rule that defines whether coupon roll dates are aligned to the maturity or
        issue date. the possible values are:   issue,   maturity,   shortfirstprorata,
        shortfirstfull,   longfirstfull,   shortlastprorata.  the default value is
        'maturity'.
    index_average_method : IndexAverageMethod, optional
        The value of the average index calculation method. the possible values are:
        compoundedactual,      dailycompoundedaverage,      compoundedaveragerate,
        arithmeticaverage
    index_observation_method : IndexObservationMethod, optional
        (rfr) method for determining the accrual observation period. the possible values
        are:      lookback: use the interest period for both rate accrual and interest
        payment.      periodshift: use the observation period for both rate accrual and
        interest payment.      mixed: use the observation period for rate accrual and
        the interest period for interest payment.
    index_spread_compounding_method : IndexSpreadCompoundingMethod, optional
        The method defining how the computed float leg spread is applied to compounded
        rate. it applies only when indexcompoundingmethod= compounded. the possible
        values are:    isdacompounding,    nocompounding,    isdaflatcompounding.  the
        default value is 'isdacompounding'.
    interest_calculation_convention : InterestCalculationConvention, optional
        The day count basis method convention used to calculate the interest payments.
        optional. defaults to moneymarket. if instrumentcode is defined, the value comes
        from the instrument reference data.
    cms_template : str, optional
        A reference to a common swap contract that represents the underlying swap in
        case of a constant maturity swap contract (cms). example: eur_ab6e. no default
        value applies.
    floor_strike_percent : float, optional
        The contractual strike rate of the floor. the value is expressed in percentages.
        if this parameter is set, the floor will apply to the leg with the same
        parameters set in the swaplegdefinition (e.g.maturity, frequency, index,
        discounting rule). no default value applies.
    index_fixing_ric : str, optional
        The ric that carries the fixing value if the instrument has a floating interest.
        optional. mandatory for floating rate instruments if no instrumentcode is
        defined. if instrumentcode is defined, the value comes from the instrument
        reference data. no default value applies.
    upfront_amount : float, optional
        The amount which represents the net present value of the swap. it is computed as
        [(100  dirtypricepercent / 100) x notionalamount]. the value is expressed in
        upfrontamountccy. by default, no payment (0) applies.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        leg_tag: Optional[str] = None,
        direction: Optional[Direction] = None,
        interest_type: Optional[InterestType] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        index_name: Optional[str] = None,
        index_tenor: Optional[str] = None,
        spread_bp: Optional[float] = None,
        interest_payment_frequency: Optional[Frequency] = None,
        interest_calculation_method: Optional[DayCountBasis] = None,
        accrued_calculation_method: Optional[DayCountBasis] = None,
        payment_business_day_convention: Optional[BusinessDayConvention] = None,
        payment_roll_convention: Optional[DateRollingConvention] = None,
        index_reset_frequency: Optional[Frequency] = None,
        index_reset_type: Optional[IndexResetType] = None,
        index_fixing_lag: Optional[int] = None,
        first_regular_payment_date: Optional[str] = None,
        last_regular_payment_date: Optional[str] = None,
        amortization_schedule: Optional[List[AmortizationItem]] = None,
        payment_business_days: Optional[str] = None,
        notional_exchange: Optional[NotionalExchange] = None,
        adjust_interest_to_payment_date: Optional[AdjustInterestToPaymentDate] = None,
        index_compounding_method: Optional[IndexCompoundingMethod] = None,
        interest_payment_delay: Optional[int] = None,
        stub_rule: Optional[StubRule] = None,
        index_average_method: Optional[IndexAverageMethod] = None,
        index_observation_method: Optional[IndexObservationMethod] = None,
        index_spread_compounding_method: Optional[IndexSpreadCompoundingMethod] = None,
        interest_calculation_convention: Optional[InterestCalculationConvention] = None,
        cms_template: Optional[str] = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        upfront_amount: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.leg_tag = leg_tag
        self.direction = direction
        self.interest_type = interest_type
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.spread_bp = spread_bp
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.accrued_calculation_method = accrued_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_reset_type = index_reset_type
        self.index_fixing_lag = index_fixing_lag
        self.first_regular_payment_date = first_regular_payment_date
        self.last_regular_payment_date = last_regular_payment_date
        self.amortization_schedule = amortization_schedule
        self.payment_business_days = payment_business_days
        self.notional_exchange = notional_exchange
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.index_compounding_method = index_compounding_method
        self.interest_payment_delay = interest_payment_delay
        self.stub_rule = stub_rule
        self.index_average_method = index_average_method
        self.index_observation_method = index_observation_method
        self.index_spread_compounding_method = index_spread_compounding_method
        self.interest_calculation_convention = interest_calculation_convention
        self.cms_template = cms_template
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.upfront_amount = upfront_amount

    @property
    def accrued_calculation_method(self):
        """
        The day count basis method used to calculate the accrued interest payments (e.g.
        dcb_30_360, dcb_30_actual).   if instrumentcode is defined, the value comes from
        the instrument reference data. in case of a user-defined instrument,
        interestcalculationmethod is used.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "accruedCalculationMethod")

    @accrued_calculation_method.setter
    def accrued_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "accruedCalculationMethod", value)

    @property
    def adjust_interest_to_payment_date(self):
        """
        An indication if the coupon dates are adjusted to the payment dates. the
        possible values are:   adjusted,   unadjusted.  if instrumentcode is defined,
        the value comes from the instrument reference data. in case of a user-defined
        instrument, the default value is 'adjusted'.
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
        information:   startdate,   enddate,   remainingnotional,
        amortizationfrequency,   amount,   amortizationtype.  optional. no default value
        applies.
        :return: list AmortizationItem
        """
        return self._get_list_parameter(AmortizationItem, "amortizationSchedule")

    @amortization_schedule.setter
    def amortization_schedule(self, value):
        self._set_list_parameter(AmortizationItem, "amortizationSchedule", value)

    @property
    def direction(self):
        """
        The indication whether the cash flows of the instrument's leg are paid or
        received. the possible values are:   paid: the cash flows are paid to the
        counterparty,   received: the cash flows are received from the counterparty.  no
        default value applies.
        :return: enum Direction
        """
        return self._get_enum_parameter(Direction, "direction")

    @direction.setter
    def direction(self, value):
        self._set_enum_parameter(Direction, "direction", value)

    @property
    def index_average_method(self):
        """
        The value of the average index calculation method. the possible values are:
        compoundedactual,      dailycompoundedaverage,      compoundedaveragerate,
        arithmeticaverage
        :return: enum IndexAverageMethod
        """
        return self._get_enum_parameter(IndexAverageMethod, "indexAverageMethod")

    @index_average_method.setter
    def index_average_method(self, value):
        self._set_enum_parameter(IndexAverageMethod, "indexAverageMethod", value)

    @property
    def index_compounding_method(self):
        """
        The method how the interest rate is calculated from the reset floating rates
        when the reset frequency is higher than the interest payment frequency (e.g.
        daily index reset with quarterly interest payments). the possible values are:
        compounded, average, constant, adjustedcompounded, mexicancompounded. if
        instrumentcode is defined, the value comes from the instrument reference data.
        in case of a user-defined instrument, the default value is 'constant'.
        :return: enum IndexCompoundingMethod
        """
        return self._get_enum_parameter(
            IndexCompoundingMethod, "indexCompoundingMethod"
        )

    @index_compounding_method.setter
    def index_compounding_method(self, value):
        self._set_enum_parameter(
            IndexCompoundingMethod, "indexCompoundingMethod", value
        )

    @property
    def index_observation_method(self):
        """
        (rfr) method for determining the accrual observation period. the possible values
        are:      lookback: use the interest period for both rate accrual and interest
        payment.      periodshift: use the observation period for both rate accrual and
        interest payment.      mixed: use the observation period for rate accrual and
        the interest period for interest payment.
        :return: enum IndexObservationMethod
        """
        return self._get_enum_parameter(
            IndexObservationMethod, "indexObservationMethod"
        )

    @index_observation_method.setter
    def index_observation_method(self, value):
        self._set_enum_parameter(
            IndexObservationMethod, "indexObservationMethod", value
        )

    @property
    def index_reset_frequency(self):
        """
        The reset frequency for the floating instrument (e.g. annual, semiannual).   the
        default value is interestpaymentfrequency.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "indexResetFrequency")

    @index_reset_frequency.setter
    def index_reset_frequency(self, value):
        self._set_enum_parameter(Frequency, "indexResetFrequency", value)

    @property
    def index_reset_type(self):
        """
        A type indicating if the floating rate index is reset before the coupon period
        starts or at the end of the coupon period. the possible values are: inadvance:
        resets the index before the start of the interest period, inarrears: resets the
        index at the end of the interest period. the default value is 'inadvance'.
        :return: enum IndexResetType
        """
        return self._get_enum_parameter(IndexResetType, "indexResetType")

    @index_reset_type.setter
    def index_reset_type(self, value):
        self._set_enum_parameter(IndexResetType, "indexResetType", value)

    @property
    def index_spread_compounding_method(self):
        """
        The method defining how the computed float leg spread is applied to compounded
        rate. it applies only when indexcompoundingmethod= compounded. the possible
        values are:    isdacompounding,    nocompounding,    isdaflatcompounding.  the
        default value is 'isdacompounding'.
        :return: enum IndexSpreadCompoundingMethod
        """
        return self._get_enum_parameter(
            IndexSpreadCompoundingMethod, "indexSpreadCompoundingMethod"
        )

    @index_spread_compounding_method.setter
    def index_spread_compounding_method(self, value):
        self._set_enum_parameter(
            IndexSpreadCompoundingMethod, "indexSpreadCompoundingMethod", value
        )

    @property
    def interest_calculation_convention(self):
        """
        The day count basis method convention used to calculate the interest payments.
        optional. defaults to moneymarket. if instrumentcode is defined, the value comes
        from the instrument reference data.
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
        The day count basis method used to calculate the interest payments(e.g.
        dcb_30_360, dcb_30_actual). the default value is selected based onnotionalccy.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "interestCalculationMethod")

    @interest_calculation_method.setter
    def interest_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "interestCalculationMethod", value)

    @property
    def interest_payment_frequency(self):
        """
        The frequency of the interest payment. either indexresetfrequency or
        interestpaymentfrequency must be provided (e.g. annual, semiannual).   the
        default value is indexresetfrequency.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "interestPaymentFrequency")

    @interest_payment_frequency.setter
    def interest_payment_frequency(self, value):
        self._set_enum_parameter(Frequency, "interestPaymentFrequency", value)

    @property
    def interest_type(self):
        """
        An indicator whether the instrument pays a fixed or floating interest. the
        possible values are: fixed, float. no default value applies.
        :return: enum InterestType
        """
        return self._get_enum_parameter(InterestType, "interestType")

    @interest_type.setter
    def interest_type(self, value):
        self._set_enum_parameter(InterestType, "interestType", value)

    @property
    def notional_exchange(self):
        """
        An indicator if the notional amount is exchanged and when it is exchanged. the
        possible values are:    none,    start,    end,    both,    endadjustment.   the
        default value is 'none'.
        :return: enum NotionalExchange
        """
        return self._get_enum_parameter(NotionalExchange, "notionalExchange")

    @notional_exchange.setter
    def notional_exchange(self, value):
        self._set_enum_parameter(NotionalExchange, "notionalExchange", value)

    @property
    def payment_business_day_convention(self):
        """
        The method to adjust dates to working days. the possible values are:
        previousbusinessday,    nextbusinessday,    modified following,    nomoving,
        bbswmodifiedfollowing.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'modifiedfollowing'.
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
        last28,    same28.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'same'.
        :return: enum DateRollingConvention
        """
        return self._get_enum_parameter(DateRollingConvention, "paymentRollConvention")

    @payment_roll_convention.setter
    def payment_roll_convention(self, value):
        self._set_enum_parameter(DateRollingConvention, "paymentRollConvention", value)

    @property
    def stub_rule(self):
        """
        The rule that defines whether coupon roll dates are aligned to the maturity or
        issue date. the possible values are:   issue,   maturity,   shortfirstprorata,
        shortfirstfull,   longfirstfull,   shortlastprorata.  the default value is
        'maturity'.
        :return: enum StubRule
        """
        return self._get_enum_parameter(StubRule, "stubRule")

    @stub_rule.setter
    def stub_rule(self, value):
        self._set_enum_parameter(StubRule, "stubRule", value)

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
    def first_regular_payment_date(self):
        """
        The first regular interest payment date used for the odd first interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
        :return: str
        """
        return self._get_parameter("firstRegularPaymentDate")

    @first_regular_payment_date.setter
    def first_regular_payment_date(self, value):
        self._set_parameter("firstRegularPaymentDate", value)

    @property
    def fixed_rate_percent(self):
        """
        The interest rate of the instrument. the value is expressed in percentages.
        mandatory if no instrumentcode is defined. if instrumentcode is defined, the
        value comes from the instrument reference data.
        :return: float
        """
        return self._get_parameter("fixedRatePercent")

    @fixed_rate_percent.setter
    def fixed_rate_percent(self, value):
        self._set_parameter("fixedRatePercent", value)

    @property
    def floor_strike_percent(self):
        """
        The contractual strike rate of the floor. the value is expressed in percentages.
        if this parameter is set, the floor will apply to the leg with the same
        parameters set in the swaplegdefinition (e.g.maturity, frequency, index,
        discounting rule). no default value applies.
        :return: float
        """
        return self._get_parameter("floorStrikePercent")

    @floor_strike_percent.setter
    def floor_strike_percent(self, value):
        self._set_parameter("floorStrikePercent", value)

    @property
    def index_fixing_lag(self):
        """
        The number of working daysbetween the fixing date and the start of the coupon
        period ('inadvance') or the end of the coupon period ('inarrears'). the
        inadvance/inarrears mode is set in the indexresettype parameter. the default
        value is the fixing lag associated to the index defined/determined by default on
        the floating instrument.
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
        optional. mandatory for floating rate instruments if no instrumentcode is
        defined. if instrumentcode is defined, the value comes from the instrument
        reference data. no default value applies.
        :return: str
        """
        return self._get_parameter("indexFixingRic")

    @index_fixing_ric.setter
    def index_fixing_ric(self, value):
        self._set_parameter("indexFixingRic", value)

    @property
    def index_name(self):
        """
        The name of the floating rate index (e.g. 'euribor'). no default value applies.
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)

    @property
    def index_tenor(self):
        """
        The period code indicating the maturity of the floating rate index. the default
        value is the tenor equivalent toindexresetfrequency or interestpaymentfrequency.
        :return: str
        """
        return self._get_parameter("indexTenor")

    @index_tenor.setter
    def index_tenor(self, value):
        self._set_parameter("indexTenor", value)

    @property
    def instrument_tag(self):
        """
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        self._set_parameter("instrumentTag", value)

    @property
    def interest_payment_delay(self):
        """
        The number of working days between the end of the interest accrual period and
        the interest payment date. by default, no delay (0) is applied.
        :return: int
        """
        return self._get_parameter("interestPaymentDelay")

    @interest_payment_delay.setter
    def interest_payment_delay(self, value):
        self._set_parameter("interestPaymentDelay", value)

    @property
    def last_regular_payment_date(self):
        """
        The last regular interest payment date used for the odd last interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
        :return: str
        """
        return self._get_parameter("lastRegularPaymentDate")

    @last_regular_payment_date.setter
    def last_regular_payment_date(self, value):
        self._set_parameter("lastRegularPaymentDate", value)

    @property
    def leg_tag(self):
        """
        A user-defined string to identify the direction of the leg: 'paid' or
        'received'. optional. no default value applies.
        :return: str
        """
        return self._get_parameter("legTag")

    @leg_tag.setter
    def leg_tag(self, value):
        self._set_parameter("legTag", value)

    @property
    def notional_amount(self):
        """
        The notional amount of the instrument's leg. the default value is '1,000,000'.
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
        4217 alphabetical format (e.g. 'usd'). no default value applies.
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
        the default value is the calendar associated to the market conventions of the
        interestpaymentccy for the corresponding leg.
        :return: str
        """
        return self._get_parameter("paymentBusinessDays")

    @payment_business_days.setter
    def payment_business_days(self, value):
        self._set_parameter("paymentBusinessDays", value)

    @property
    def spread_bp(self):
        """
        The interest spread in basis points that is added to the floating rate index
        value. optional. if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is '0'.
        :return: float
        """
        return self._get_parameter("spreadBp")

    @spread_bp.setter
    def spread_bp(self, value):
        self._set_parameter("spreadBp", value)

    @property
    def upfront_amount(self):
        """
        The amount which represents the net present value of the swap. it is computed as
        [(100  dirtypricepercent / 100) x notionalamount]. the value is expressed in
        upfrontamountccy. by default, no payment (0) applies.
        :return: float
        """
        return self._get_parameter("upfrontAmount")

    @upfront_amount.setter
    def upfront_amount(self, value):
        self._set_parameter("upfrontAmount", value)
