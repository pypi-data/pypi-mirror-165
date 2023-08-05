# coding: utf8


from typing import Optional

from ..._object_definition import ObjectDefinition
from ._enums import PriceSide


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    price_side : PriceSide, optional
        The quoted price side of the instrument. optional. default value is 'mid'.
    exercise_date : str, optional

    market_data_date : str, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The market value of the instrument. the value is expressed in the deal currency.
        optional. no default value applies. note that premium takes priority over
        volatility input.
    nb_iterations : int, optional
        The number of steps for the bermudan swaption pricing via the hull-white
        one-factor (hw1f) tree.  no default value applies.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    simulate_exercise : bool, optional
        Tells if in case of future cashflows should be considered as exercised or not.
        possible values:    true,    false.
    valuation_date : str, optional
        The valuation date for pricing. If not set the valuation date is equal to
        market_data_date or Today. For assets that contains a settlementConvention,
        the default valuation date  is equal to the settlementdate of the Asset that is
        usually the TradeDate+SettlementConvention.

    Examples
    --------
     >>> import refinitiv.data.content.ipa.financial_contracts as rdf
     >>> rdf.swaption.PricingParameters(valuation_date="2020-04-24", nb_iterations=80)
    """

    def __init__(
        self,
        price_side: Optional[PriceSide] = None,
        exercise_date: Optional[str] = None,
        market_data_date: Optional[str] = None,
        market_value_in_deal_ccy: Optional[float] = None,
        nb_iterations: Optional[int] = None,
        report_ccy: Optional[str] = None,
        simulate_exercise: Optional[bool] = None,
        valuation_date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.price_side = price_side
        self.exercise_date = exercise_date
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.nb_iterations = nb_iterations
        self.report_ccy = report_ccy
        self.simulate_exercise = simulate_exercise
        self.valuation_date = valuation_date

    @property
    def price_side(self):
        """
        The quoted price side of the instrument. optional. default value is 'mid'.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def exercise_date(self):
        """
        :return: str
        """
        return self._get_parameter("exerciseDate")

    @exercise_date.setter
    def exercise_date(self, value):
        self._set_parameter("exerciseDate", value)

    @property
    def market_data_date(self):
        """
        The market data date for pricing.
        By default, the marketDataDate date is the ValuationDate or Today.
        :return: str
        """
        return self._get_parameter("marketDataDate")

    @market_data_date.setter
    def market_data_date(self, value):
        self._set_parameter("marketDataDate", value)

    @property
    def market_value_in_deal_ccy(self):
        """
        MarketValueInDealCcy to override and that will be used as pricing analysis input to compute VolatilityPercent.
        No override is applied by default. Note that Premium takes priority over Volatility input.
        :return: float
        """
        return self._get_parameter("marketValueInDealCcy")

    @market_value_in_deal_ccy.setter
    def market_value_in_deal_ccy(self, value):
        self._set_parameter("marketValueInDealCcy", value)

    @property
    def nb_iterations(self):
        """
        Used for Bermudans and HW1F tree.
        :return: int
        """
        return self._get_parameter("nbIterations")

    @nb_iterations.setter
    def nb_iterations(self, value):
        self._set_parameter("nbIterations", value)

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
    def simulate_exercise(self):
        """
        Tells if in case of future cashflows should be considered as exercised or not.
        possible values:    true,    false.
        :return: bool
        """
        return self._get_parameter("simulateExercise")

    @simulate_exercise.setter
    def simulate_exercise(self, value):
        self._set_parameter("simulateExercise", value)

    @property
    def valuation_date(self):
        """
        The valuation date for pricing.
        If not set the valuation date is equal to MarketDataDate or Today.
        For assets that contains a settlementConvention, the default valuation date  is equal to
        the settlementdate of the Asset that is usually the TradeDate+SettlementConvention.
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_parameter("valuationDate", value)
