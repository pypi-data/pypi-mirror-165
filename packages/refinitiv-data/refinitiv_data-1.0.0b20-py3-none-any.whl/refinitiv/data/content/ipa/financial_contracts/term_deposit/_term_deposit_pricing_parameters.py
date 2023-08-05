# coding: utf8

from typing import Optional

from ._enums import PriceSide
from ..._object_definition import ObjectDefinition


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    price_side : PriceSide, optional
        Price Side to consider when retrieving Market Data.
    income_tax_percent : float, optional
        Income tax percent is subtracted from applied interest rate percents at the end
        of the deposit. Example: "5" means 5%
        By default is 0.
    market_data_date : str, optional
        The market data date for pricing.
        By default, the market_data_date date is the valuation_date or Today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). It is set for the fields ending with 'xxxinreportccy'. Optional. The
        default value is the notional currency.
    valuation_date : str, optional
        The valuation date for pricing. If not set the valuation date is equal to
        market_data_date or Today. For assets that contains a settlementConvention, the
        default valuation date  is equal to the settlementdate of the Asset that is
        usually the TradeDate+SettlementConvention.

    Examples
    --------
     >>> import refinitiv.data.content.ipa.financial_contracts as rdf
     >>> rdf.term_deposit.PricingParameters(valuation_date="2020-04-24")
    """

    def __init__(
        self,
        price_side: Optional[PriceSide] = None,
        income_tax_percent: Optional[float] = None,
        market_data_date: Optional[str] = None,
        report_ccy: Optional[str] = None,
        valuation_date: Optional[str] = None,
    ):
        super().__init__()
        self.price_side = price_side
        self.income_tax_percent = income_tax_percent
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    @property
    def price_side(self):
        """
        Price Side to consider when retrieving Market Data.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def income_tax_percent(self):
        """
        Income tax percent is substracted from applied interest rate percents in the end of deposit.
        Example: "5" means 5%
        :return: float
        """
        return self._get_parameter("incomeTaxPercent")

    @income_tax_percent.setter
    def income_tax_percent(self, value):
        self._set_parameter("incomeTaxPercent", value)

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
