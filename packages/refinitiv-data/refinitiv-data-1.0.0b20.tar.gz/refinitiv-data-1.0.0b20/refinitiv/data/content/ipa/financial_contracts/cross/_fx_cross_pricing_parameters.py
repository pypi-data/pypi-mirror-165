# coding: utf8

from typing import Optional

from ._enums import PriceSide, FxSwapCalculationMethod, ImpliedDepositDateConvention
from ..._object_definition import ObjectDefinition


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    fx_swap_calculation_method : FxSwapCalculationMethod, optional
        The method used to calculate an outright price or deposit rates. the possible
        values are:
        - fxswap: outrights are computed using swap points,
        - fxswapimpliedfromdeposit: implied fx swap points are computed from deposit
          rates.  optional. defaults to 'fxswap'.
    implied_deposit_date_convention : ImpliedDepositDateConvention, optional
        An indicator for the "depositccy1impliedfromfxswap",
        "depositccy2impliedfromfxswap" calculation methods, used to check whether dts or
        dtm period is selected for the implied deposits calculation. by default, for the
        implied deposits calculation we use the dts(day to spot) period, while for the
        deposits the dtm(day to money market) period is used. the possible values are:
        - fxmarketconvention:    dts case, traditional method getperiodsfromtenor is
          used with the parameter "from:fxtrade"
        - moneymarketconvention: dtm case, getperiodsfromtenor with the parameter
          "from:mmtrade" is used optional.
    price_side : PriceSide, optional
        The quoted price side of the instrument. the possible values are:
        - bid,
        - ask,
        - mid. optional. defaults to 'mid'.
    adjust_all_deposit_points_to_cross_calendars : bool, optional
        An indicator if depositccy1marketdata and depositccy2marketdata are adjusted to
        the cross calendar dates. the possible values are:
        - true: the market data is adjusted according to the cross calendar dates,
        - false: unmodified market data is returned, cross calendar is ignored.
          optional. defaults to 'false'.
    adjust_all_swap_points_to_cross_calendars : bool, optional
        An indicator if fxswapsccy1 and fxswapsccy2 are adjusted to the cross calendar
        dates. the possible values are:
        - true: the market data is adjusted according to the cross calendar dates,
        - false: unmodified market data is returned, cross calendar is ignored.
          optional. defaults to 'false'.
    ignore_ref_ccy_holidays : bool, optional
        An indicator if holidays of the reference currency are included or not in the
        pricing when dates are computed. by default, the reference currency is usd. the
        possible values are:
        - true: holidays are ignored,
        - false: holidays are included in pricing. optional. defaults to 'false'.
    market_data_date : str, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    use_direct_quote : bool, optional
        An indicator if the spot and the swap points should be retrieved without a pivot
        currency
        - true: the market data is retrieved directly
        - false: unmodified market data is returned. optional. defaults to 'false'.
    valuation_date : str, optional
        The valuation date for pricing.  Optional. If not set the valuation date is
        equal to market_data_date or Today. For assets that contains a
        settlementConvention, the default valuation date  is equal to the settlementdate
        of the Asset that is usually the TradeDate+SettlementConvention.
    """

    def __init__(
        self,
        fx_swap_calculation_method: Optional[FxSwapCalculationMethod] = None,
        implied_deposit_date_convention: Optional[ImpliedDepositDateConvention] = None,
        price_side: Optional[PriceSide] = None,
        adjust_all_deposit_points_to_cross_calendars: Optional[bool] = None,
        adjust_all_swap_points_to_cross_calendars: Optional[bool] = None,
        ignore_ref_ccy_holidays: Optional[bool] = None,
        market_data_date: Optional[str] = None,
        report_ccy: Optional[str] = None,
        use_direct_quote: Optional[bool] = None,
        valuation_date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_deposit_date_convention = implied_deposit_date_convention
        self.price_side = price_side
        self.adjust_all_deposit_points_to_cross_calendars = (
            adjust_all_deposit_points_to_cross_calendars
        )
        self.adjust_all_swap_points_to_cross_calendars = (
            adjust_all_swap_points_to_cross_calendars
        )
        self.ignore_ref_ccy_holidays = ignore_ref_ccy_holidays
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.use_direct_quote = use_direct_quote
        self.valuation_date = valuation_date

    @property
    def fx_swap_calculation_method(self):
        """
        The method we chose to price outright using or not implied deposits. Possible
        values are:   FxSwap (compute outright using swap points),
        DepositCcy1ImpliedFromFxSwap (compute currency1 deposits using swap points),
        DepositCcy2ImpliedFromFxSwap (compute currency2 deposits using swap points).
        Optional. Defaults to 'FxSwap'.
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
    def implied_deposit_date_convention(self):
        """
        :return: object FxPoint
        """
        return self._get_enum_parameter(
            ImpliedDepositDateConvention, "impliedDepositDateConvention"
        )

    @implied_deposit_date_convention.setter
    def implied_deposit_date_convention(self, value):
        self._set_enum_parameter(
            ImpliedDepositDateConvention, "impliedDepositDateConvention", value
        )

    @property
    def price_side(self):
        """
        The type of price returned for pricing Analysis:
        Bid(Bid value),
        Ask(Ask value),
        Mid(Mid value)
        Optional. Defaults to 'Mid'.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def adjust_all_deposit_points_to_cross_calendars(self):
        """
        An indicator if depositccy1marketdata and depositccy2marketdata are adjusted to
        the cross calendar dates. the possible values are:
        - true: the market data is adjusted according to the cross calendar dates,
        - false: unmodified market data is returned, cross calendar is ignored.
          optional. defaults to 'false'.
        :return: bool
        """
        return self._get_parameter("adjustAllDepositPointsToCrossCalendars")

    @adjust_all_deposit_points_to_cross_calendars.setter
    def adjust_all_deposit_points_to_cross_calendars(self, value):
        self._set_parameter("adjustAllDepositPointsToCrossCalendars", value)

    @property
    def adjust_all_swap_points_to_cross_calendars(self):
        """
        This flag define if cross-calendar holidays should be taken into account for
        fx_swaps_ccy1 and fx_swaps_ccy2. it adjusts swap points according to cross
        holidays if it's set to true, by default set to false.
        :return: bool
        """
        return self._get_parameter("adjustAllSwapPointsToCrossCalendars")

    @adjust_all_swap_points_to_cross_calendars.setter
    def adjust_all_swap_points_to_cross_calendars(self, value):
        self._set_parameter("adjustAllSwapPointsToCrossCalendars", value)

    @property
    def ignore_ref_ccy_holidays(self):
        """
        The reference currency holidays flag : When dates are computed, its possible to
        choose if holidays of the reference currency are included or not in the pricing
        Optional. Defaults to 'false'.
        :return: bool
        """
        return self._get_parameter("ignoreRefCcyHolidays")

    @ignore_ref_ccy_holidays.setter
    def ignore_ref_ccy_holidays(self, value):
        self._set_parameter("ignoreRefCcyHolidays", value)

    @property
    def market_data_date(self):
        """
        The market data date for pricing. Optional. By default, the market_data_date
        date is the valuation_date or Today
        :return: str
        """
        return self._get_parameter("marketDataDate")

    @market_data_date.setter
    def market_data_date(self, value):
        self._set_parameter("marketDataDate", value)

    @property
    def report_ccy(self):
        """
        :return: str
        """
        return self._get_parameter("reportCcy")

    @report_ccy.setter
    def report_ccy(self, value):
        self._set_parameter("reportCcy", value)

    @property
    def use_direct_quote(self):
        """
        An indicator if the spot and the swap points should be retrieved without a pivot
        currency
        - true: the market data is retrieved directly
        - false: unmodified market data is returned. optional. defaults to 'false'.
        :return: bool
        """
        return self._get_parameter("useDirectQuote")

    @use_direct_quote.setter
    def use_direct_quote(self, value):
        self._set_parameter("useDirectQuote", value)

    @property
    def valuation_date(self):
        """
        The valuation date for pricing.  Optional. If not set the valuation date is
        equal to market_data_date or Today. For assets that contains a
        settlementConvention, the default valuation date  is equal to the settlementdate
        of the Asset that is usually the TradeDate+SettlementConvention.
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_parameter("valuationDate", value)
