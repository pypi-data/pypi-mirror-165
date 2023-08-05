from typing import Optional, List, Union

from ._custom_instruments_data_provider import is_instrument_id, get_user_id
from ._stream_facade import Stream
from .._content_type import ContentType
from ..._tools import universe_arg_parser
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod


class Definition:
    """
    Allows to create custom instrument, symbol and formula fields are mandatory, others are optional

    Parameters
    -----------
    universe : str
        The Id or Symbol of custom instrument to operate on. Use only for get_instrument().
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import Definition
    >>> definition = Definition(universe="MyNewInstrument")
    >>> stream = definition.get_stream()
    """

    def __init__(
        self,
        universe: Optional[Union[str, List[str]]],
        extended_params: Optional[dict] = None,
    ):
        extended_params = extended_params or {}
        universe = extended_params.pop("universe", universe)
        self.universe = universe_arg_parser.get_list(universe)
        self._extended_params = extended_params

    def get_stream(self, session=None) -> Stream:
        stream = Stream(
            universe=self.universe,
            session=session,
            extended_params=self._extended_params,
        )
        return stream
