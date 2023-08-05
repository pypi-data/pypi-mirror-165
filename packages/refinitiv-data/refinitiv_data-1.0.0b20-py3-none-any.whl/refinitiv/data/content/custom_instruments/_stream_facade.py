import re
from typing import Any, Callable, List, Optional, TYPE_CHECKING, Union

from ._custom_instruments_data_provider import get_user_id, is_instrument_id
from .._content_type import ContentType
from .._universe_streams import UniverseStreamFacade, _UniverseStreams
from ..._tools import (
    PRICING_DATETIME_PATTERN,
    cached_property,
    create_repr,
    make_callback,
)
from ..._tools._dataframe import convert_df_columns_to_datetime_use_re_compile
from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod
from ...delivery._stream.base_stream import StreamOpenWithUpdatesMixin

if TYPE_CHECKING:
    import pandas
    from ... import OpenState
    from ..._core.session import Session


def _init_universe(universe, session):
    uuid = None
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
    )

    result = []
    for symbol in universe:
        if is_instrument_id.match(symbol):
            instrument_response = data_provider_layer.get_data(
                session, method=RequestMethod.GET
            )
            symbol = instrument_response.data.raw.get("symbol")
            if not uuid:
                uuid = symbol.rsplit(".", 1)[-1]

        else:
            if not symbol.startswith("S)"):
                symbol = f"S){symbol}"
            if "." not in symbol:
                if not uuid:
                    uuid = get_user_id(session)
                symbol = f"{symbol}.{uuid}"
        result.append(symbol)
    return result


class CustomInstrumentsStream(UniverseStreamFacade):
    pass


class Stream(StreamOpenWithUpdatesMixin):
    def __init__(
        self,
        session: "Session" = None,
        universe: Union[str, List[str]] = None,
        fields: Optional[list] = None,
        service: Optional[str] = None,
        extended_params: Optional[dict] = None,
    ) -> None:
        self._session = session
        self._universe = universe or []
        self._fields = fields
        self._service = service
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> _UniverseStreams:
        return _UniverseStreams(
            content_type=ContentType.STREAMING_CUSTOM_INSTRUMENTS,
            item_facade_class=CustomInstrumentsStream,
            universe=self._universe,
            session=self._session,
            fields=self._fields,
            service=self._service,
            extended_params=self._extended_params,
        )

    def open(self, with_updates: bool = True) -> "OpenState":
        self._universe = _init_universe(self._universe, self._session)
        self._stream.open(with_updates=with_updates)
        return self.open_state

    def close(self) -> "OpenState":
        self._stream.close()
        return self.open_state

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        _fields = {
            universe: {
                key: value
                for key, value in self._stream[universe].items()
                if fields is None or key in fields
            }
        }
        return _fields

    def get_snapshot(
        self,
        universe: Union[str, List[str], None] = None,
        fields: Optional[List[str]] = None,
        convert: bool = True,
    ) -> "pandas.DataFrame":
        df = self._stream.get_snapshot(
            universe=universe, fields=fields, convert=convert
        )
        convert_df_columns_to_datetime_use_re_compile(df, PRICING_DATETIME_PATTERN)
        return df

    def on_refresh(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_refresh(make_callback(func))
        return self

    def on_update(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_update(make_callback(func))
        return self

    def on_status(self, func: Callable[[Any, str, "Stream"], Any]) -> "Stream":
        self._stream.on_status(make_callback(func))
        return self

    def on_complete(self, func: Callable[["Stream"], Any]) -> "Stream":
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable) -> "Stream":
        self._stream.on_error(make_callback(func))
        return self

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, item) -> "UniverseStreamFacade":
        return self._stream.__getitem__(item)

    def __len__(self) -> int:
        return self._stream.__len__()

    def __repr__(self):
        return create_repr(
            self,
            class_name=self.__class__.__name__,
            content=f"{{name='{self._universe}'}}",
        )
