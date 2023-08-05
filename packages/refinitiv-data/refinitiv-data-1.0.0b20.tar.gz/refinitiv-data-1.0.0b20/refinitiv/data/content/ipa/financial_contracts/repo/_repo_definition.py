# coding: utf8

from typing import Optional

from .._instrument_definition import InstrumentDefinition
from ._enums import (
    BuySell,
    DayCountBasis,
)
from ._repo_underlying_contract import UnderlyingContract


class RepoInstrumentDefinition(InstrumentDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.it can be used to link output
        results to the instrument definition. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    start_date : str, optional
        Start date of the repo, that means when the underlying security is exchanged.
        mandatory.
    end_date : str, optional
        End date of the repo, that means when the borrower repurchases the security
        back. either enddate or tenor field are requested.
    tenor : str, optional
        Tenor that defines the duration of the repo in case no enddate has been
        provided. in that case, enddate is computed from startdate and tenor. either
        enddate or tenor field are requested.
    buy_sell : BuySell, optional
        The indicator of the deal side. the possible values are:   buy: buying the repo,
        sell: selling the repo.  optional. the default value is "buy".
    day_count_basis : DayCountBasis, optional
        Day count basis convention to apply to the custom repo rate. optional,
        "dcb_actual_360" by default.
    underlying_instruments : RepoUnderlyingContract, optional
        Definition of the underlying instruments. only bond contracts are supported for
        now, and only one bond can be used. mandatory.
    is_coupon_exchanged : bool, optional
        Specifies whether or not intermediate coupons are exchanged.
        - couponexchanged = true to specify that intermediate coupons for the underlying
          bond (between the repo start date and repo end date) are exchanged between the
          repo seller and repo buyer.
        - couponexchanged = false to specify that no intermediate coupons are exchanged
          between the repo seller and repo buyer. in this case the repo instrument is
          like a standard loan with no intermediate coupons; the bond is only used as a
          warranty in case the money borrower defaults. optional. true by default, which
          means coupon exchanged.
    repo_rate_percent : float, optional
        Custom repo rate in percentage. if not provided in the request, it will be
        computed by interpolating/extrapolating a repo curve. optional.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        buy_sell: Optional[BuySell] = None,
        day_count_basis: Optional[DayCountBasis] = None,
        underlying_instruments: Optional[UnderlyingContract] = None,
        is_coupon_exchanged: Optional[bool] = None,
        repo_rate_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.buy_sell = buy_sell
        self.day_count_basis = day_count_basis
        self.underlying_instruments = underlying_instruments
        self.is_coupon_exchanged = is_coupon_exchanged
        self.repo_rate_percent = repo_rate_percent

    @classmethod
    def get_instrument_type(cls):
        return "Repo"

    @property
    def buy_sell(self):
        """
        The indicator of the deal side. the possible values are:   buy: buying the repo,
        sell: selling the repo.  optional. the default value is "buy".
        :return: enum BuySell
        """
        return self._get_enum_parameter(BuySell, "buySell")

    @buy_sell.setter
    def buy_sell(self, value):
        self._set_enum_parameter(BuySell, "buySell", value)

    @property
    def day_count_basis(self):
        """
        Day count basis convention to apply to the custom repo rate. optional,
        "dcb_actual_360" by default.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "dayCountBasis")

    @day_count_basis.setter
    def day_count_basis(self, value):
        self._set_enum_parameter(DayCountBasis, "dayCountBasis", value)

    @property
    def underlying_instruments(self):
        """
        Definition of the underlying instruments. only bond contracts are supported for
        now, and only one bond can be used. mandatory.
        :return: list RepoUnderlyingContract
        """
        return self._get_list_parameter(UnderlyingContract, "underlyingInstruments")

    @underlying_instruments.setter
    def underlying_instruments(self, value):
        self._set_list_parameter(UnderlyingContract, "underlyingInstruments", value)

    @property
    def end_date(self):
        """
        End date of the repo, that means when the borrower repurchases the security
        back. either enddate or tenor field are requested.
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
    def is_coupon_exchanged(self):
        """
        Specifies whether or not intermediate coupons are exchanged.
        - couponexchanged = true to specify that intermediate coupons for the underlying
          bond (between the repo start date and repo end date) are exchanged between the
          repo seller and repo buyer.
        - couponexchanged = false to specify that no intermediate coupons are exchanged
          between the repo seller and repo buyer. in this case the repo instrument is
          like a standard loan with no intermediate coupons; the bond is only used as a
          warranty in case the money borrower defaults. optional. true by default, which
          means coupon exchanged.
        :return: bool
        """
        return self._get_parameter("isCouponExchanged")

    @is_coupon_exchanged.setter
    def is_coupon_exchanged(self, value):
        self._set_parameter("isCouponExchanged", value)

    @property
    def repo_rate_percent(self):
        """
        Custom repo rate in percentage. if not provided in the request, it will be
        computed by interpolating/extrapolating a repo curve. optional.
        :return: float
        """
        return self._get_parameter("repoRatePercent")

    @repo_rate_percent.setter
    def repo_rate_percent(self, value):
        self._set_parameter("repoRatePercent", value)

    @property
    def start_date(self):
        """
        Start date of the repo, that means when the underlying security is exchanged.
        mandatory.
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_parameter("startDate", value)

    @property
    def tenor(self):
        """
        Tenor that defines the duration of the repo in case no enddate has been
        provided. in that case, enddate is computed from startdate and tenor. either
        enddate or tenor field are requested.
        :return: str
        """
        return self._get_parameter("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_parameter("tenor", value)
