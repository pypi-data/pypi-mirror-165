# coding: utf8

from typing import Optional, List

from ..._object_definition import ObjectDefinition

from ._enums import (
    FxSwapCalculationMethod,
    OptionVolatilityType,
    PriceSide,
    PricingModelType,
    TimeStamp,
    VolatilityModel,
)
from ._models import (
    BidAskMid,
    InterpolationWeight,
    PayoutScaling,
)


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    atm_volatility_object : BidAskMid, optional

    butterfly10_d_object : BidAskMid, optional

    butterfly25_d_object : BidAskMid, optional

    domestic_deposit_rate_percent_object : BidAskMid, optional

    foreign_deposit_rate_percent_object : BidAskMid, optional

    forward_points_object : BidAskMid, optional

    fx_spot_object : BidAskMid, optional

    fx_swap_calculation_method : FxSwapCalculationMethod, optional
        The method used to calculate an outright price or deposit rates. the possible
        values are:
        - fxswapimpliedfromdeposit: implied fx swap points are computed from deposit
          rates.
        - depositccy1impliedfromfxswap: currency 1 deposit rates are computed using swap
          points,
        - depositccy2impliedfromfxswap: currency 2 deposit rates are computed using swap
          points.  the default value is 'depositccy2impliedfromfxswap'.
    implied_volatility_object : BidAskMid, optional

    interpolation_weight : InterpolationWeight, optional

    option_price_side : PriceSide, optional
        The quoted price side of the instrument.the possible values are:
        - bid,
        - ask,
        - mid,
        - last. optional. the default values for listed options are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided. the default value for otc options is 'mid'.
    option_time_stamp : TimeStamp, optional
        The mode of the instrument's timestamp selection. the possible values are:
        - open: the opening value of valuationdate, or if it is not available, the close
          of the previous day is used,
        - close: the close value of valuationdate is used,
        - default: the latest snapshot is used when valuationdate is today, and the
          close price when valuationdate is in the past. optional.the default value is
          'default'.
    payout_custom_dates : string, optional
        The array of dates set by a user for the payout/volatility chart. optional.no
        default value applies.
    payout_scaling_interval : PayoutScaling, optional

    price_side : PriceSide, optional
        The quoted price side of the instrument. the possible values are:
        - bid,
        - ask,
        - mid.
    pricing_model_type : PricingModelType, optional
        The model type of the option pricing. the possible values are:
        - blackscholes
        - bachelier (available for commodity options including calendar spread options)
        - whaley
        - binomial
        - trinomial
        - localvolatility (applicable only for barrier options, cbbc options and binary
          options)
        - vannavolga (only applicable for fxbarrieroption, fxdigitaloption and
          fxtouchesoption)  optional. the default value depends on the option type.
    risk_reversal10_d_object : BidAskMid, optional

    risk_reversal25_d_object : BidAskMid, optional

    underlying_price_side : PriceSide, optional
        The quoted price side of the underlying asset.the possible values are:
        - bid,
        - ask,
        - mid,
        - last. optional. the default values are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided.
    underlying_time_stamp : TimeStamp, optional
        The mode of the underlying asset's timestamp selection. the possible values are:
        - open: the opening value of valuationdate, or if it is not available, the close
          of the previous day is used,
        - close: the close value of valuationdate is used,
        - default: the latest snapshot is used when valuationdate is today, and the
          close price when valuationdate is in the past. optional.the default value is
          'default'.
    volatility_model : VolatilityModel, optional
        The model used to build the volatility surface. the possible values are:
        - sabr,
        - cubicspline,
        - svi,
        - twinlognormal,
        - vannavolga10d,
        - vannavolga25d.
    volatility_type : OptionVolatilityType, optional
        The type of volatility for the option pricing. the possible values are:
        - implied: the volatility anticipated for the underlying asset for the remaining
          life of the option(implied by an option premium),
        - svisurface: the volatility computed from volsurface service,
        - historical: the volatility of the underlying asset during a period in the
          past. the value 'implied' is available only for listed options. if
          volatilitypercent is defined, volatilitytype is not taken into account.
          optional. the default value is 'implied'.
    compute_payout_chart : bool, optional
        Define whether the payout chart must be computed or not
    compute_volatility_payout : bool, optional
        Define whether the volatility payout chart must be computed or not
    cutoff_time : str, optional
        The cutoff time
    cutoff_time_zone : str, optional
        The cutoff time zone
    market_data_date : str, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The market value (premium) of the instrument. the value is expressed in the deal
        currency. it is used to define optionprice and compute volatilitypercent. if
        marketvalueindealccy is defined, optionpriceside and volatilitypercent are not
        taken into account; marketvalueindealccy and marketvalueinreportccy cannot be
        overriden at a time. optional. by default, it is equal to optionprice for listed
        options or computed from volatilitypercent for otc options.
    market_value_in_report_ccy : float, optional
        The market value (premium) of the instrument. it is computed as
        [marketvalueindealccy  fxspot]. the value is expressed in the reporting
        currency. it is used to define optionprice and computevolatilitypercent.
        ifmarketvalueinreportccyis defined, optionpriceside and volatilitypercentinputs
        are not taken into account; marketvalueindealccy and marketvalueinreportccy
        cannot be overriden at a time. optional. by default, fxspot rate is retrieved
        from the market data.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    report_ccy_rate : float, optional
        The rate of the reporting currency against the option currency. it can be used
        to calculate optionprice and marketvalueindealccy if marketvalueinreportccy is
        defined. optional.by default, it is retrieved from the market data.
    risk_free_rate_percent : float, optional
        A risk-free rate of the option currency used for the option pricing. optional.
        by default, the value is retrieved from the market data.
    simulate_exercise : bool, optional
        Tells if payoff-linked cashflow should be returned. possible values:
        - true
        - false
    underlying_price : float, optional
        The price of the underlying asset. the value is expressed in the deal currency.
        if underlyingprice is defined, underlyingpriceside is not taken into account.
        optional. by default, the value is retrieved from the market data.
    valuation_date : str, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    volatility : float, optional
        Volatility(without unity) to override and that will be used as pricing analysis
        input to compute marketvalueindealccy. introduced due to bachelier model, for
        more details please have a look at apqps-13558 optional. no override is applied
        by default. note that if premium is defined, volatility is not taken into
        account.
    volatility_percent : float, optional
        The degree of the underlying asset's price variations over a specified time
        period, used for the option pricing. the value is expressed in percentages. it
        is used to compute marketvalueindealccy.if marketvalueindealccy is defined,
        volatilitypercent is not taken into account. optional. by default, it is
        computed from marketvalueindealccy. if volsurface fails to return a volatility,
        it defaults to '20'.
    """

    def __init__(
        self,
        atm_volatility_object: Optional[BidAskMid] = None,
        butterfly10_d_object: Optional[BidAskMid] = None,
        butterfly25_d_object: Optional[BidAskMid] = None,
        domestic_deposit_rate_percent_object: Optional[BidAskMid] = None,
        foreign_deposit_rate_percent_object: Optional[BidAskMid] = None,
        forward_points_object: Optional[BidAskMid] = None,
        fx_spot_object: Optional[BidAskMid] = None,
        fx_swap_calculation_method: Optional[FxSwapCalculationMethod] = None,
        implied_volatility_object: Optional[BidAskMid] = None,
        interpolation_weight: Optional[InterpolationWeight] = None,
        option_price_side: Optional[PriceSide] = None,
        option_time_stamp: Optional[TimeStamp] = None,
        payout_custom_dates: Optional[List[str]] = None,
        payout_scaling_interval: Optional[PayoutScaling] = None,
        price_side: Optional[PriceSide] = None,
        pricing_model_type: Optional[PricingModelType] = None,
        risk_reversal10_d_object: Optional[BidAskMid] = None,
        risk_reversal25_d_object: Optional[BidAskMid] = None,
        underlying_price_side: Optional[PriceSide] = None,
        underlying_time_stamp: Optional[TimeStamp] = None,
        volatility_model: Optional[VolatilityModel] = None,
        volatility_type: Optional[OptionVolatilityType] = None,
        compute_payout_chart: Optional[bool] = None,
        compute_volatility_payout: Optional[bool] = None,
        cutoff_time: Optional[str] = None,
        cutoff_time_zone: Optional[str] = None,
        market_data_date: Optional[str] = None,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
        report_ccy: Optional[str] = None,
        report_ccy_rate: Optional[float] = None,
        risk_free_rate_percent: Optional[float] = None,
        simulate_exercise: Optional[bool] = None,
        underlying_price: Optional[float] = None,
        valuation_date: Optional[str] = None,
        volatility: Optional[float] = None,
        volatility_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.atm_volatility_object = atm_volatility_object
        self.butterfly10_d_object = butterfly10_d_object
        self.butterfly25_d_object = butterfly25_d_object
        self.domestic_deposit_rate_percent_object = domestic_deposit_rate_percent_object
        self.foreign_deposit_rate_percent_object = foreign_deposit_rate_percent_object
        self.forward_points_object = forward_points_object
        self.fx_spot_object = fx_spot_object
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_volatility_object = implied_volatility_object
        self.interpolation_weight = interpolation_weight
        self.option_price_side = option_price_side
        self.option_time_stamp = option_time_stamp
        self.payout_custom_dates = payout_custom_dates
        self.payout_scaling_interval = payout_scaling_interval
        self.price_side = price_side
        self.pricing_model_type = pricing_model_type
        self.risk_reversal10_d_object = risk_reversal10_d_object
        self.risk_reversal25_d_object = risk_reversal25_d_object
        self.underlying_price_side = underlying_price_side
        self.underlying_time_stamp = underlying_time_stamp
        self.volatility_model = volatility_model
        self.volatility_type = volatility_type
        self.compute_payout_chart = compute_payout_chart
        self.compute_volatility_payout = compute_volatility_payout
        self.cutoff_time = cutoff_time
        self.cutoff_time_zone = cutoff_time_zone
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.market_value_in_report_ccy = market_value_in_report_ccy
        self.report_ccy = report_ccy
        self.report_ccy_rate = report_ccy_rate
        self.risk_free_rate_percent = risk_free_rate_percent
        self.simulate_exercise = simulate_exercise
        self.underlying_price = underlying_price
        self.valuation_date = valuation_date
        self.volatility = volatility
        self.volatility_percent = volatility_percent

    @property
    def atm_volatility_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "atmVolatilityObject")

    @atm_volatility_object.setter
    def atm_volatility_object(self, value):
        self._set_object_parameter(BidAskMid, "atmVolatilityObject", value)

    @property
    def butterfly10_d_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "butterfly10DObject")

    @butterfly10_d_object.setter
    def butterfly10_d_object(self, value):
        self._set_object_parameter(BidAskMid, "butterfly10DObject", value)

    @property
    def butterfly25_d_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "butterfly25DObject")

    @butterfly25_d_object.setter
    def butterfly25_d_object(self, value):
        self._set_object_parameter(BidAskMid, "butterfly25DObject", value)

    @property
    def domestic_deposit_rate_percent_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "domesticDepositRatePercentObject")

    @domestic_deposit_rate_percent_object.setter
    def domestic_deposit_rate_percent_object(self, value):
        self._set_object_parameter(BidAskMid, "domesticDepositRatePercentObject", value)

    @property
    def foreign_deposit_rate_percent_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "foreignDepositRatePercentObject")

    @foreign_deposit_rate_percent_object.setter
    def foreign_deposit_rate_percent_object(self, value):
        self._set_object_parameter(BidAskMid, "foreignDepositRatePercentObject", value)

    @property
    def forward_points_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "forwardPointsObject")

    @forward_points_object.setter
    def forward_points_object(self, value):
        self._set_object_parameter(BidAskMid, "forwardPointsObject", value)

    @property
    def fx_spot_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "fxSpotObject")

    @fx_spot_object.setter
    def fx_spot_object(self, value):
        self._set_object_parameter(BidAskMid, "fxSpotObject", value)

    @property
    def fx_swap_calculation_method(self):
        """
        The method used to calculate an outright price or deposit rates. the possible
        values are:
        - fxswapimpliedfromdeposit: implied fx swap points are computed from deposit
          rates.
        - depositccy1impliedfromfxswap: currency 1 deposit rates are computed using swap
          points,
        - depositccy2impliedfromfxswap: currency 2 deposit rates are computed using swap
          points.  the default value is 'depositccy2impliedfromfxswap'.
        :return: enum FxSwapCalculationMethod
        """
        return self._get_enum_parameter(
            FxSwapCalculationMethod, "fxSwapCalculationMethod"
        )

    @fx_swap_calculation_method.setter
    def fx_swap_calculation_method(self, value):
        self._set_enum_parameter(
            FxSwapCalculationMethod, "fxSwapCalculationMethod", value
        )

    @property
    def implied_volatility_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "impliedVolatilityObject")

    @implied_volatility_object.setter
    def implied_volatility_object(self, value):
        self._set_object_parameter(BidAskMid, "impliedVolatilityObject", value)

    @property
    def interpolation_weight(self):
        """
        :return: object InterpolationWeight
        """
        return self._get_object_parameter(InterpolationWeight, "interpolationWeight")

    @interpolation_weight.setter
    def interpolation_weight(self, value):
        self._set_object_parameter(InterpolationWeight, "interpolationWeight", value)

    @property
    def option_price_side(self):
        """
        The quoted price side of the instrument.the possible values are:
        - bid,
        - ask,
        - mid,
        - last. optional. the default values for listed options are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided. the default value for otc options is 'mid'.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "optionPriceSide")

    @option_price_side.setter
    def option_price_side(self, value):
        self._set_enum_parameter(PriceSide, "optionPriceSide", value)

    @property
    def option_time_stamp(self):
        """
        The mode of the instrument's timestamp selection. the possible values are:
        - open: the opening value of valuationdate, or if it is not available, the close
          of the previous day is used,
        - close: the close value of valuationdate is used,
        - default: the latest snapshot is used when valuationdate is today, and the
          close price when valuationdate is in the past. optional.the default value is
          'default'.
        :return: enum TimeStamp
        """
        return self._get_enum_parameter(TimeStamp, "optionTimeStamp")

    @option_time_stamp.setter
    def option_time_stamp(self, value):
        self._set_enum_parameter(TimeStamp, "optionTimeStamp", value)

    @property
    def payout_custom_dates(self):
        """
        The array of dates set by a user for the payout/volatility chart. optional.no
        default value applies.
        :return: list string
        """
        return self._get_list_parameter(str, "payoutCustomDates")

    @payout_custom_dates.setter
    def payout_custom_dates(self, value):
        self._set_list_parameter(str, "payoutCustomDates", value)

    @property
    def payout_scaling_interval(self):
        """
        :return: object PayoutScaling
        """
        return self._get_object_parameter(PayoutScaling, "payoutScalingInterval")

    @payout_scaling_interval.setter
    def payout_scaling_interval(self, value):
        self._set_object_parameter(PayoutScaling, "payoutScalingInterval", value)

    @property
    def price_side(self):
        """
        The quoted price side of the instrument. the possible values are:
        - bid,
        - ask,
        - mid.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def pricing_model_type(self):
        """
        The model type of the option pricing. the possible values are:
        - blackscholes
        - bachelier (available for commodity options including calendar spread options)
        - whaley
        - binomial
        - trinomial
        - localvolatility (applicable only for barrier options, cbbc options and binary
          options)
        - vannavolga (only applicable for fxbarrieroption, fxdigitaloption and
          fxtouchesoption)  optional. the default value depends on the option type.
        :return: enum PricingModelType
        """
        return self._get_enum_parameter(PricingModelType, "pricingModelType")

    @pricing_model_type.setter
    def pricing_model_type(self, value):
        self._set_enum_parameter(PricingModelType, "pricingModelType", value)

    @property
    def risk_reversal10_d_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "riskReversal10DObject")

    @risk_reversal10_d_object.setter
    def risk_reversal10_d_object(self, value):
        self._set_object_parameter(BidAskMid, "riskReversal10DObject", value)

    @property
    def risk_reversal25_d_object(self):
        """
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "riskReversal25DObject")

    @risk_reversal25_d_object.setter
    def risk_reversal25_d_object(self, value):
        self._set_object_parameter(BidAskMid, "riskReversal25DObject", value)

    @property
    def underlying_price_side(self):
        """
        The quoted price side of the underlying asset.the possible values are:
        - bid,
        - ask,
        - mid,
        - last. optional. the default values are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "underlyingPriceSide")

    @underlying_price_side.setter
    def underlying_price_side(self, value):
        self._set_enum_parameter(PriceSide, "underlyingPriceSide", value)

    @property
    def underlying_time_stamp(self):
        """
        The mode of the underlying asset's timestamp selection. the possible values are:
        - open: the opening value of valuationdate, or if it is not available, the close
          of the previous day is used,
        - close: the close value of valuationdate is used,
        - default: the latest snapshot is used when valuationdate is today, and the
          close price when valuationdate is in the past. optional.the default value is
          'default'.
        :return: enum TimeStamp
        """
        return self._get_enum_parameter(TimeStamp, "underlyingTimeStamp")

    @underlying_time_stamp.setter
    def underlying_time_stamp(self, value):
        self._set_enum_parameter(TimeStamp, "underlyingTimeStamp", value)

    @property
    def volatility_model(self):
        """
        The model used to build the volatility surface. the possible values are:
        - sabr,
        - cubicspline,
        - svi,
        - twinlognormal,
        - vannavolga10d,
        - vannavolga25d.
        :return: enum VolatilityModel
        """
        return self._get_enum_parameter(VolatilityModel, "volatilityModel")

    @volatility_model.setter
    def volatility_model(self, value):
        self._set_enum_parameter(VolatilityModel, "volatilityModel", value)

    @property
    def volatility_type(self):
        """
        The type of volatility for the option pricing. the possible values are:
        - implied: the volatility anticipated for the underlying asset for the remaining
          life of the option(implied by an option premium),
        - svisurface: the volatility computed from volsurface service,
        - historical: the volatility of the underlying asset during a period in the
          past. the value 'implied' is available only for listed options. if
          volatilitypercent is defined, volatilitytype is not taken into account.
          optional. the default value is 'implied'.
        :return: enum OptionVolatilityType
        """
        return self._get_enum_parameter(OptionVolatilityType, "volatilityType")

    @volatility_type.setter
    def volatility_type(self, value):
        self._set_enum_parameter(OptionVolatilityType, "volatilityType", value)

    @property
    def compute_payout_chart(self):
        """
        Define whether the payout chart must be computed or not
        :return: bool
        """
        return self._get_parameter("computePayoutChart")

    @compute_payout_chart.setter
    def compute_payout_chart(self, value):
        self._set_parameter("computePayoutChart", value)

    @property
    def compute_volatility_payout(self):
        """
        Define whether the volatility payout chart must be computed or not
        :return: bool
        """
        return self._get_parameter("computeVolatilityPayout")

    @compute_volatility_payout.setter
    def compute_volatility_payout(self, value):
        self._set_parameter("computeVolatilityPayout", value)

    @property
    def cutoff_time(self):
        """
        The cutoff time
        :return: str
        """
        return self._get_parameter("cutoffTime")

    @cutoff_time.setter
    def cutoff_time(self, value):
        self._set_parameter("cutoffTime", value)

    @property
    def cutoff_time_zone(self):
        """
        The cutoff time zone
        :return: str
        """
        return self._get_parameter("cutoffTimeZone")

    @cutoff_time_zone.setter
    def cutoff_time_zone(self, value):
        self._set_parameter("cutoffTimeZone", value)

    @property
    def market_data_date(self):
        """
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
        :return: str
        """
        return self._get_parameter("marketDataDate")

    @market_data_date.setter
    def market_data_date(self, value):
        self._set_parameter("marketDataDate", value)

    @property
    def market_value_in_deal_ccy(self):
        """
        The market value (premium) of the instrument. the value is expressed in the deal
        currency. it is used to define optionprice and compute volatilitypercent. if
        marketvalueindealccy is defined, optionpriceside and volatilitypercent are not
        taken into account; marketvalueindealccy and marketvalueinreportccy cannot be
        overriden at a time. optional. by default, it is equal to optionprice for listed
        options or computed from volatilitypercent for otc options.
        :return: float
        """
        return self._get_parameter("marketValueInDealCcy")

    @market_value_in_deal_ccy.setter
    def market_value_in_deal_ccy(self, value):
        self._set_parameter("marketValueInDealCcy", value)

    @property
    def market_value_in_report_ccy(self):
        """
        The market value (premium) of the instrument. it is computed as
        [marketvalueindealccy  fxspot]. the value is expressed in the reporting
        currency. it is used to define optionprice and computevolatilitypercent.
        ifmarketvalueinreportccyis defined, optionpriceside and volatilitypercentinputs
        are not taken into account; marketvalueindealccy and marketvalueinreportccy
        cannot be overriden at a time. optional. by default, fxspot rate is retrieved
        from the market data.
        :return: float
        """
        return self._get_parameter("marketValueInReportCcy")

    @market_value_in_report_ccy.setter
    def market_value_in_report_ccy(self, value):
        self._set_parameter("marketValueInReportCcy", value)

    @property
    def report_ccy(self):
        """
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
        :return: str
        """
        return self._get_parameter("reportCcy")

    @report_ccy.setter
    def report_ccy(self, value):
        self._set_parameter("reportCcy", value)

    @property
    def report_ccy_rate(self):
        """
        The rate of the reporting currency against the option currency. it can be used
        to calculate optionprice and marketvalueindealccy if marketvalueinreportccy is
        defined. optional.by default, it is retrieved from the market data.
        :return: float
        """
        return self._get_parameter("reportCcyRate")

    @report_ccy_rate.setter
    def report_ccy_rate(self, value):
        self._set_parameter("reportCcyRate", value)

    @property
    def risk_free_rate_percent(self):
        """
        A risk-free rate of the option currency used for the option pricing. optional.
        by default, the value is retrieved from the market data.
        :return: float
        """
        return self._get_parameter("riskFreeRatePercent")

    @risk_free_rate_percent.setter
    def risk_free_rate_percent(self, value):
        self._set_parameter("riskFreeRatePercent", value)

    @property
    def simulate_exercise(self):
        """
        Tells if payoff-linked cashflow should be returned. possible values:
        - true
        - false
        :return: bool
        """
        return self._get_parameter("simulateExercise")

    @simulate_exercise.setter
    def simulate_exercise(self, value):
        self._set_parameter("simulateExercise", value)

    @property
    def underlying_price(self):
        """
        The price of the underlying asset. the value is expressed in the deal currency.
        if underlyingprice is defined, underlyingpriceside is not taken into account.
        optional. by default, the value is retrieved from the market data.
        :return: float
        """
        return self._get_parameter("underlyingPrice")

    @underlying_price.setter
    def underlying_price(self, value):
        self._set_parameter("underlyingPrice", value)

    @property
    def valuation_date(self):
        """
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_parameter("valuationDate", value)

    @property
    def volatility(self):
        """
        Volatility(without unity) to override and that will be used as pricing analysis
        input to compute marketvalueindealccy. introduced due to bachelier model, for
        more details please have a look at apqps-13558 optional. no override is applied
        by default. note that if premium is defined, volatility is not taken into
        account.
        :return: float
        """
        return self._get_parameter("volatility")

    @volatility.setter
    def volatility(self, value):
        self._set_parameter("volatility", value)

    @property
    def volatility_percent(self):
        """
        The degree of the underlying asset's price variations over a specified time
        period, used for the option pricing. the value is expressed in percentages. it
        is used to compute marketvalueindealccy.if marketvalueindealccy is defined,
        volatilitypercent is not taken into account. optional. by default, it is
        computed from marketvalueindealccy. if volsurface fails to return a volatility,
        it defaults to '20'.
        :return: float
        """
        return self._get_parameter("volatilityPercent")

    @volatility_percent.setter
    def volatility_percent(self, value):
        self._set_parameter("volatilityPercent", value)
