# coding: utf8


from typing import Optional

from ._enums import (
    IndexConvexityAdjustmentIntegrationMethod,
    IndexConvexityAdjustmentMethod,
    PriceSide,
    TenorReferenceDate,
)
from ..._object_definition import ObjectDefinition


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    index_convexity_adjustment_integration_method : IndexConvexityAdjustmentIntegrationMethod, optional
        The integration method used for static replication method. the possible values
        are: riemannsum, rungekutta. the default value is 'riemannsum'.
    index_convexity_adjustment_method : IndexConvexityAdjustmentMethod, optional
        The convexity adjustment type for constant maturity swaps (cms) and libor
        in-arrears swaps. the possible values are: none, blackscholes, linearswapmodel,
        replication. the default value is 'blackscholes'.
    price_side : PriceSide, optional
        The quoted price side of the instrument. optional. default value is 'mid'.
    tenor_reference_date : TenorReferenceDate, optional
        In case the swap definition uses 'starttenor', 'starttenor' defines whether the
        swap start date is calculated from valuation date or from spot date
    discounting_ccy : str, optional
        The currency code, which defines the choice of the discounting curve. the value
        is expressed in iso 4217 alphabetical format (e.g. 'usd'). by default,
        settlementccy or the paid leg currency is used.
    discounting_tenor : str, optional

    market_data_date : str, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The dirty market value of the instrument computed as
        [cleanmarketvalueindealccy+accruedamountindealccy]. the value is expressed in
        the deal currency. the default value is '0'.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    use_legs_signing : bool, optional
        Enable the signing of "risk measures" and "valuation" outputs based on leg's
        direction the default value is false.
    valuation_date : str, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    """

    def __init__(
        self,
        index_convexity_adjustment_integration_method: Optional[
            IndexConvexityAdjustmentIntegrationMethod
        ] = None,
        index_convexity_adjustment_method: Optional[
            IndexConvexityAdjustmentMethod
        ] = None,
        price_side: Optional[PriceSide] = None,
        tenor_reference_date: Optional[TenorReferenceDate] = None,
        discounting_ccy: Optional[str] = None,
        discounting_tenor: Optional[str] = None,
        market_data_date: Optional[str] = None,
        market_value_in_deal_ccy: Optional[float] = None,
        report_ccy: Optional[str] = None,
        use_legs_signing: Optional[bool] = None,
        valuation_date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.index_convexity_adjustment_integration_method = (
            index_convexity_adjustment_integration_method
        )
        self.index_convexity_adjustment_method = index_convexity_adjustment_method
        self.price_side = price_side
        self.tenor_reference_date = tenor_reference_date
        self.discounting_ccy = discounting_ccy
        self.discounting_tenor = discounting_tenor
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.report_ccy = report_ccy
        self.use_legs_signing = use_legs_signing
        self.valuation_date = valuation_date

    @property
    def index_convexity_adjustment_integration_method(self):
        """
        The integration method used for static replication method. the possible values
        are: riemannsum, rungekutta. the default value is 'riemannsum'.
        :return: enum IndexConvexityAdjustmentIntegrationMethod
        """
        return self._get_enum_parameter(
            IndexConvexityAdjustmentIntegrationMethod,
            "indexConvexityAdjustmentIntegrationMethod",
        )

    @index_convexity_adjustment_integration_method.setter
    def index_convexity_adjustment_integration_method(self, value):
        self._set_enum_parameter(
            IndexConvexityAdjustmentIntegrationMethod,
            "indexConvexityAdjustmentIntegrationMethod",
            value,
        )

    @property
    def index_convexity_adjustment_method(self):
        """
        The convexity adjustment type for constant maturity swaps (cms) and libor
        in-arrears swaps. the possible values are: none, blackscholes, linearswapmodel,
        replication. the default value is 'blackscholes'.
        :return: enum IndexConvexityAdjustmentMethod
        """
        return self._get_enum_parameter(
            IndexConvexityAdjustmentMethod, "indexConvexityAdjustmentMethod"
        )

    @index_convexity_adjustment_method.setter
    def index_convexity_adjustment_method(self, value):
        self._set_enum_parameter(
            IndexConvexityAdjustmentMethod, "indexConvexityAdjustmentMethod", value
        )

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
    def tenor_reference_date(self):
        """
        In case the swap definition uses 'starttenor', 'starttenor' defines whether the
        swap start date is calculated from valuation date or from spot date
        :return: enum TenorReferenceDate
        """
        return self._get_enum_parameter(TenorReferenceDate, "tenorReferenceDate")

    @tenor_reference_date.setter
    def tenor_reference_date(self, value):
        self._set_enum_parameter(TenorReferenceDate, "tenorReferenceDate", value)

    @property
    def discounting_ccy(self):
        """
        The currency code, which defines the choice of the discounting curve. the value
        is expressed in iso 4217 alphabetical format (e.g. 'usd'). by default,
        settlementccy or the paid leg currency is used.
        :return: str
        """
        return self._get_parameter("discountingCcy")

    @discounting_ccy.setter
    def discounting_ccy(self, value):
        self._set_parameter("discountingCcy", value)

    @property
    def discounting_tenor(self):
        """
        :return: str
        """
        return self._get_parameter("discountingTenor")

    @discounting_tenor.setter
    def discounting_tenor(self, value):
        self._set_parameter("discountingTenor", value)

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
        The dirty market value of the instrument computed as
        [cleanmarketvalueindealccy+accruedamountindealccy]. the value is expressed in
        the deal currency. the default value is '0'.
        :return: float
        """
        return self._get_parameter("marketValueInDealCcy")

    @market_value_in_deal_ccy.setter
    def market_value_in_deal_ccy(self, value):
        self._set_parameter("marketValueInDealCcy", value)

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
    def use_legs_signing(self):
        """
        Enable the signing of "risk measures" and "valuation" outputs based on leg's
        direction the default value is false.
        :return: bool
        """
        return self._get_parameter("useLegsSigning")

    @use_legs_signing.setter
    def use_legs_signing(self, value):
        self._set_parameter("useLegsSigning", value)

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
