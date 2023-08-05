from typing import Union, Optional, Iterable, TYPE_CHECKING

from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value
from ....delivery._data._data_provider import (
    DataProviderLayer,
    BaseResponse,
    UniverseData,
)

if TYPE_CHECKING:
    from ....content._types import ExtendedParams

optional_date = Optional[Union[str, "datetime.datetime"]]


class Definition(DataProviderLayer[BaseResponse[UniverseData]]):
    """
    This class describe parameters to retrieve details on stakeholders and strategic entities
    transactions that purchased the requested instruments. Further details of insider stakeholder
    can be requested along with their holding details. The operation supports pagination, however,
    it is dependent on user entitlements. Maximum 'count' value per page is 100. The default date
    range is 20 transactions, unless the 'start date' and 'end date' define a smaller range. The
    count value is checked by the service to determine if it does not exceed a specific number. If
    it does, the service will overwrite the client value to service default value.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the single company for which the content is returned.

    start: str, datetime, optional
        The start parameter allows users to define the start date of a time series.
        Dates are to be defined either by absolute or relative syntax.
        Example, 20190529, -1Q, 1D, -3MA.

    end: str, datetime, optional
        The end parameter allows users to define the start date of a time series.
        Dates are to be defined either by absolute or relative syntax.
        Example, 20190529, -1Q, 1D, -3MA.

    limit: int, optional
        The limit parameter is used for paging. It allows users to select the number of records to be returned.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.insider.transaction_report.Definition("TRI.N", start="-1Q")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        start: optional_date = None,
        end: optional_date = None,
        limit: Optional[int] = None,
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(limit, [int, type(None)], "limit")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT,
            universe=universe,
            start=start,
            end=end,
            limit=limit,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
