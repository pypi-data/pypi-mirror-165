# coding: utf8

from typing import Optional

from ._enums import RepoCurveType
from ..._object_definition import ObjectDefinition


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    repo_curve_type : RepoCurveType, optional
        Curve used to compute the repo rate. it can be computed using following methods:
        - repocurve : rate is computed by interpolating a repo curve.     - depositcurve
        : rate is computed by interpolating a deposit curve.     - fixinglibor : rate is
        computed by interpolating libor rates.  if no curve can be found, the rate is
        computed using a deposit curve.
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
        repo_curve_type: Optional[RepoCurveType] = None,
        market_data_date: Optional[str] = None,
        report_ccy: Optional[str] = None,
        valuation_date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.repo_curve_type = repo_curve_type
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    @property
    def repo_curve_type(self):
        """
        Curve used to compute the repo rate. it can be computed using following methods:
        - repocurve : rate is computed by interpolating a repo curve.     - depositcurve
        : rate is computed by interpolating a deposit curve.     - fixinglibor : rate is
        computed by interpolating libor rates.  if no curve can be found, the rate is
        computed using a deposit curve.
        :return: enum RepoCurveType
        """
        return self._get_enum_parameter(RepoCurveType, "repoCurveType")

    @repo_curve_type.setter
    def repo_curve_type(self, value):
        self._set_enum_parameter(RepoCurveType, "repoCurveType", value)

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
