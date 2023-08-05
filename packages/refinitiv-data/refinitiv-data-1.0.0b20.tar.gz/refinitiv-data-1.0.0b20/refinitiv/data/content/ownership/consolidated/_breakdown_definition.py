from typing import Iterable, Union, TYPE_CHECKING

from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value
from .._enums import StatTypes
from ....delivery._data._data_provider import (
    DataProviderLayer,
    BaseResponse,
    UniverseData,
)

if TYPE_CHECKING:
    from ....content._types import ExtendedParams


class Definition(DataProviderLayer[BaseResponse[UniverseData]]):
    """
    This class describe parameters to retrieve holdings data breakdown by Investor Types,
    Styles, Region, Countries, Rotations and Turnovers.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    stat_type: int, StatTypes
        The statType parameter specifies which statistics type to be returned.
        The types available are:
            - Investor Type (1)
            - Investment Style (2)
            - Region (3)
            - Rotation (4)
            - Country (5)
            - Metro Area (6)
            - Investor Type Parent (7)
            - Invest Style Parent (8)

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params: ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.consolidated.breakdown.Definition("TRI.N", ownership.StatTypes.INVESTOR_TYPE)
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        stat_type: Union[int, StatTypes],
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(stat_type, [int, StatTypes], "stat_type")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN,
            universe=universe,
            stat_type=stat_type,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
