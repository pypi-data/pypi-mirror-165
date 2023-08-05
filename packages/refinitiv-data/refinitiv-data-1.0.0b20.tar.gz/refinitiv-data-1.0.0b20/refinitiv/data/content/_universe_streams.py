import itertools
from concurrent.futures import ThreadPoolExecutor, wait
from typing import (
    Union,
    Iterable,
    Callable,
    Dict,
    KeysView,
    ValuesView,
    Tuple,
    ItemsView,
    Optional,
)

import pandas as pd

from ._types import Strings, OptBool
from ._universe_stream import _UniverseStream
from .._core.session import get_valid_session, Session
from .._errors import ItemWasNotRequested
from .._tools import universe_arg_parser, fields_arg_parser, cached_property
from ..delivery._stream import (
    StreamStateManager,
    OMMStreamListener,
    StreamStateEvent,
    StreamEvent,
)
from ..delivery._stream.base_stream import StreamOpenWithUpdatesMixin

_id_iterator = itertools.count()


def build_df(
    universe: Strings, fields: Strings, values_by_field: dict, convert: bool
) -> pd.DataFrame:
    data = (
        (inst_name, *(values.pop(0) or pd.NA for values in values_by_field.values()))
        for inst_name in universe
    )

    df = pd.DataFrame(data=data, columns=("Instrument", *fields))

    if convert:
        df = df.convert_dtypes()

    return df


def validate(name, input_values, requested_values):
    input_values = set(input_values)
    requested_values = set(requested_values)
    not_requested = input_values - requested_values
    has_not_requested = bool(not_requested)

    if has_not_requested:
        raise ItemWasNotRequested(name, not_requested, requested_values)


def get_available_fields(value_by_fields_by_inst_names):
    available_fields = []
    for value_by_fields in value_by_fields_by_inst_names.values():
        fields = value_by_fields.keys()
        available_fields.extend(fields)
    return list(dict.fromkeys(available_fields))


class UniverseStreamFacade(StreamOpenWithUpdatesMixin):
    def __init__(self, stream: _UniverseStream):
        self._stream: _UniverseStream = stream

    @property
    def id(self) -> int:
        return self._stream.id

    @property
    def code(self):
        return self._stream.code

    @property
    def message(self):
        return self._stream.message

    @property
    def name(self):
        return self._stream.name

    @property
    def service(self):
        return self._stream.service

    @property
    def fields(self):
        return self._stream.fields

    @property
    def status(self):
        return self._stream.status

    @property
    def is_ok(self):
        return self._stream.is_ok

    def __enter__(self):
        return self._stream.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stream.__exit__(exc_type, exc_val, exc_tb)

    def get_field_value(self, field):
        return self._stream.get_field_value(field)

    def get_fields(self, fields=None) -> dict:
        return self._stream.get_fields(fields)

    def keys(self):
        return self._stream.keys()

    def values(self):
        return self._stream.values()

    def items(self):
        return self._stream.items()

    def __iter__(self):
        return self._stream.__iter__()

    def __getitem__(self, field):
        try:
            item = self._stream.__getitem__(field)
        except KeyError:
            item = None
        return item

    def __len__(self):
        return self._stream.__len__()

    def __repr__(self):
        return self._stream.__repr__()

    def __str__(self):
        return self._stream.__str__()


class _UniverseStreams(StreamStateManager, OMMStreamListener):
    def __init__(
        self,
        content_type,
        universe: Union[str, Iterable[str]],
        item_facade_class=UniverseStreamFacade,
        session: "Session" = None,
        fields: Union[str, list] = None,
        service: str = None,
        on_refresh: Callable = None,
        on_status: Callable = None,
        on_update: Callable = None,
        on_complete: Callable = None,
        extended_params: dict = None,
    ) -> None:
        session = get_valid_session(session)

        StreamStateManager.__init__(self, logger=session.logger())
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
        )

        self._universe: Strings = universe_arg_parser.get_list(universe)
        self._session = session
        self.fields: Strings = fields_arg_parser.get_list(fields or [])
        self._service = service
        self._extended_params = extended_params
        self._id = next(_id_iterator)
        self._classname: str = (
            f"[{self.__class__.__name__} id={self._id} universe={universe}]"
        )
        self._completed = set()
        self._content_type = content_type
        self._item_facade_class = item_facade_class

    @property
    def universe(self):
        return self._universe

    @cached_property
    def _stream_by_name(self) -> Dict[str, _UniverseStream]:
        retval = {}
        for name in self.universe:
            stream = _UniverseStream(
                content_type=self._content_type,
                session=self._session,
                name=name,
                fields=self.fields,
                service=self._service,
                on_refresh=self._on_stream_refresh,
                on_status=self._on_stream_status,
                on_update=self._on_stream_update,
                on_complete=self._on_stream_complete,
                on_error=self._on_stream_error,
                extended_params=self._extended_params,
                parent_id=self._id,
            )

            stream.on(StreamStateEvent.CLOSED, self._on_stream_close)
            retval[name] = stream
        return retval

    def keys(self) -> KeysView[str]:
        return self._stream_by_name.keys()

    def values(self) -> ValuesView[_UniverseStream]:
        return self._stream_by_name.values()

    def items(self) -> ItemsView[str, _UniverseStream]:
        return self._stream_by_name.items()

    def __iter__(self):
        return StreamIterator(self)

    def __getitem__(self, name) -> Union[_UniverseStream, dict, UniverseStreamFacade]:
        stream = self._stream_by_name.get(name, {})

        if stream == {}:
            self._warning(f"'{name}' not in {self._classname} universe")
            return stream

        if hasattr(stream, "_wrapper"):
            wrapper = stream._wrapper
        else:
            wrapper = self._item_facade_class(stream)
            stream._wrapper = wrapper

        return wrapper

    def __len__(self):
        return len(self._stream_by_name)

    def _get_value_by_fields_by_inst_names(
        self, universe: "Strings", fields: "Strings"
    ) -> dict:
        retval = {}
        for name in universe:
            stream = self._stream_by_name.get(name)

            values_by_fields = stream.get_fields(fields)
            if values_by_fields:
                retval[name] = values_by_fields
        return retval

    def get_snapshot(
        self,
        universe: Optional[Union[str, Strings]] = None,
        fields: Optional[Union[str, Strings]] = None,
        convert: OptBool = True,
    ) -> pd.DataFrame:
        """
        Returns a Dataframe filled with snapshot values
        for a list of instrument names and a list of fields.

        Parameters
        ----------
        universe: list of strings
            List of instruments to request snapshot data on.

        fields: str or list of strings
            List of fields to request.

        convert: boolean
            If True, force numeric conversion for all values.

        Returns
        -------
            pandas.DataFrame

            pandas.DataFrame content:
                - columns : instrument and field names
                - rows : instrument name and field values

        Raises
        ------
            Exception
                If request fails or if server returns an error

            ValueError
                If a parameter type or value is wrong

        """

        if universe:
            universe = universe_arg_parser.get_list(universe)
            try:
                validate("Instrument", universe, self.universe)
            except ItemWasNotRequested as e:
                self._error(e)
                return pd.DataFrame()
        else:
            universe = self.universe

        value_by_fields_by_inst_names: dict = self._get_value_by_fields_by_inst_names(
            universe, fields
        )

        if fields:
            fields = fields_arg_parser.get_unique(fields or [])

            try:
                self.fields and validate("Field", fields, self.fields)
            except ItemWasNotRequested as e:
                self._error(e)
                return pd.DataFrame()
        else:
            fields = get_available_fields(value_by_fields_by_inst_names)

        values_by_field = {
            field: [
                value_by_fields_by_inst_names.get(name, {}).get(field)
                for name in universe
            ]
            for field in fields
        }

        return build_df(universe, fields, values_by_field, convert)

    def _do_open(self, *args, with_updates=True) -> None:
        self._debug(f"{self._classname} open streaming on {self.universe}")

        if not self.values():
            raise ValueError("No instrument to subscribe")

        self._completed.clear()

        with ThreadPoolExecutor(
            thread_name_prefix="OpenUniverseStreams-Thread"
        ) as executor:
            futures = [
                executor.submit(stream.open, with_updates=with_updates)
                for stream in self.values()
            ]
            wait(futures)
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception

        self._debug(f"{self._classname} streaming on {self.universe} is open")

    def _do_close(self, *args, **kwargs) -> None:
        self._debug(f"{self._classname} close streaming on {str(self.universe)}")

        with ThreadPoolExecutor(
            thread_name_prefix="CloseUniverseStreams-Thread"
        ) as executor:
            futures = [executor.submit(stream.close) for stream in self.values()]
            wait(futures)
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception

    def _on_stream_close(self, stream) -> None:
        self._debug(f"{self._classname} streaming closed name={stream.name}")
        self.close()

    def _do_on_stream_refresh(self, stream, *args) -> Tuple:
        return self._do_on_stream(stream, *args)

    def _on_stream_status(self, stream, *args) -> None:
        self._debug(f"{self._classname} on_status {args}")

        status = args[0]
        self._emitter.emit(StreamEvent.STATUS, self, stream.name, status)

        if stream.is_closed:
            self.dispatch_complete(stream)

    def _do_on_stream_update(self, stream, *args) -> Tuple:
        return self._do_on_stream(stream, *args)

    def _do_on_stream(self, stream, *args) -> Tuple:
        fields = args[0]
        return stream.name, fields

    def _on_stream_complete(self, stream, *args) -> None:
        self._debug(f"{self._classname} on_complete {args}")

        name = stream.name
        if name in self._completed:
            return

        self._completed.update([name])
        if self._completed == set(self.universe):
            # received complete event from all streams all, emit global complete
            self._emitter.emit(StreamEvent.COMPLETE, self)

    def _do_on_stream_error(self, stream, *args) -> Tuple:
        error = args[0]
        return stream.name, error


class StreamIterator:
    def __init__(self, stream: _UniverseStreams):
        self._streaming_prices = stream
        self._index = 0

    def __next__(self):
        if self._index < len(self._streaming_prices._universe):
            result = self._streaming_prices[
                self._streaming_prices._universe[self._index]
            ]
            self._index += 1
            return result
        raise StopIteration()
