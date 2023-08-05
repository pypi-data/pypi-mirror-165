# coding: utf8

from typing import Optional, Iterable, List

from ._repo_definition import RepoInstrumentDefinition
from ._repo_pricing_parameters import PricingParameters
from ._repo_underlying_contract import UnderlyingContract
from .._base_definition import BaseDefinition
from ..._enums import DayCountBasis, BuySell
from ...._types import ExtendedParams, Strings
from ....._tools import create_repr


class Definition(BaseDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported.
    start_date : str, optional
        Start date of the repo, that means when the the underlying security is
        exchanged.
    end_date : str, optional
        End date of the repo, that means when the borrower repurchases the security
        back. Either end_date or tenor field are requested.
    tenor : str, optional
        tenor that defines the duration of the Repo in case no end_date has been
        provided. In that case, end_date is computed from start_date and tenor. Either
        end_date or tenor field are requested.
     buy_sell : BuySell, optional
        The indicator of the deal side. the possible values are:   buy: buying the repo,
        sell: selling the repo.  optional. the default value is "buy".
    day_count_basis : DayCountBasis, optional
        Day Count Basis convention to apply to the custom Repo rate.
        By default "Dcb_Actual_360".
    underlying_instruments : list of UnderlyingContract
        Definition of the underlying instruments. Only Bond Contracts are supported for
        now, and only one Bond can be used.
    is_coupon_exchanged : bool, optional
        Specifies whether or not intermediate coupons are exchanged.
        - CouponExchanged = True to specify that intermediate coupons for the underlying
          bond (between the repo start date and repo end date) are exchanged between the
          repo seller and repo buyer.
        - CouponExchanged = False to specify that no intermediate coupons are exchanged
          between the repo seller and repo buyer. In this case the repo instrument is
          like a standard loan with no intermediate coupons; the bond is only used as a
          warranty in case the money borrower defaults. True by default, which means
          coupon exchanged.
    repo_rate_percent : float, optional
        Custom Repo Rate in percentage. If not provided in the request, it will be
        computed by interpolating/extrapolating a Repo Curve.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. If pricing parameters
        are not provided at this level parameters defined globally at the request
        level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    get_data(session=session, on_response=on_response, async_mode=None)
        Returns a response to the data platform
    get_data_async(session=session, on_response=on_response, async_mode=None)
        Returns a response to the async data platform
    get_stream(session=session, api="")
        Get stream quantitative analytic service subscription

    Examples
    --------
     >>> import refinitiv.data.content.ipa.financial_contracts as rdf
     >>> definition = rdf.repo.Definition(
     ...   underlying_instruments=[
     ...   rdf.repo.UnderlyingContract(
     ...   instrument_type="Bond",
     ...   instrument_definition=rdf.bond.Definition(instrument_code="US191450264="),
     ...   )],
     ...)
     >>> response = definition.get_data()

     Using get_stream
     >>> stream = definition.get_stream()
     >>> stream.open()
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        buy_sell: Optional[BuySell] = None,
        day_count_basis: Optional[DayCountBasis] = None,
        underlying_instruments: Optional[List[UnderlyingContract]] = None,
        is_coupon_exchanged: Optional[bool] = None,
        repo_rate_percent: Optional[float] = None,
        fields: Optional[Strings] = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: ExtendedParams = None,
    ) -> None:
        self.underlying_instruments = underlying_instruments
        definition = RepoInstrumentDefinition(
            buy_sell=buy_sell,
            day_count_basis=day_count_basis,
            underlying_instruments=underlying_instruments,
            end_date=end_date,
            instrument_tag=instrument_tag,
            is_coupon_exchanged=is_coupon_exchanged,
            repo_rate_percent=repo_rate_percent,
            start_date=start_date,
            tenor=tenor,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.ipa.financial_contract",
            content=f"{{underlying_instruments='{self.underlying_instruments}'}}",
        )
