# coding: utf8

from typing import Optional

from ..._object_definition import ObjectDefinition

from ._repo_parameters import RepoParameters
from ..bond import PricingParameters as BondPricingParameters


class UnderlyingPricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    pricing_parameters_at_end : BondPricingParameters, optional

    pricing_parameters_at_start : BondPricingParameters, optional

    repo_parameters : RepoParameters, optional

    market_data_date : str, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    valuation_date : str, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    """

    def __init__(
        self,
        pricing_parameters_at_end: Optional[BondPricingParameters] = None,
        pricing_parameters_at_start: Optional[BondPricingParameters] = None,
        repo_parameters: Optional[RepoParameters] = None,
        market_data_date: Optional[str] = None,
        report_ccy: Optional[str] = None,
        valuation_date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.pricing_parameters_at_end = pricing_parameters_at_end
        self.pricing_parameters_at_start = pricing_parameters_at_start
        self.repo_parameters = repo_parameters
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    @property
    def pricing_parameters_at_end(self):
        """
        :return: object BondPricingParameters
        """
        return self._get_object_parameter(
            BondPricingParameters, "pricingParametersAtEnd"
        )

    @pricing_parameters_at_end.setter
    def pricing_parameters_at_end(self, value):
        self._set_object_parameter(
            BondPricingParameters, "pricingParametersAtEnd", value
        )

    @property
    def pricing_parameters_at_start(self):
        """
        :return: object BondPricingParameters
        """
        return self._get_object_parameter(
            BondPricingParameters, "pricingParametersAtStart"
        )

    @pricing_parameters_at_start.setter
    def pricing_parameters_at_start(self, value):
        self._set_object_parameter(
            BondPricingParameters, "pricingParametersAtStart", value
        )

    @property
    def repo_parameters(self):
        """
        :return: object RepoParameters
        """
        return self._get_object_parameter(RepoParameters, "repoParameters")

    @repo_parameters.setter
    def repo_parameters(self, value):
        self._set_object_parameter(RepoParameters, "repoParameters", value)

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
