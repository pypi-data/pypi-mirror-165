from typing import Iterable, Union, TYPE_CHECKING
from typing import Optional

from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value
from ....delivery._data._data_provider import (
    DataProviderLayer,
    BaseResponse,
    UniverseData,
)

if TYPE_CHECKING:
    from ....content._types import ExtendedParams


class Definition(DataProviderLayer[BaseResponse[UniverseData]]):
    """
    This class describe parameters to retrieve company ownership details. Also, information on
    the top 20 fund shareholders invested in the requested company.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    limit: int, optional
        The limit parameter is used for paging. It allows users to select the number of records to be returned.
        Default page size is 100 or 20 (depending on the operation).

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.fund.investors.Definition("TRI.N")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        limit: Optional[int] = None,
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(limit, [int, type(None)], "limit")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            ContentType.OWNERSHIP_FUND_INVESTORS,
            universe=universe,
            limit=limit,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
