from typing import Union, TYPE_CHECKING
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from .stream_state import StreamState
from ..._open_state import OpenState

if TYPE_CHECKING:
    from ...content.ipa.financial_contracts._quantitative_data_stream import (
        QuantitativeDataStream,
    )
    from ...content.trade_data_service._stream import TradeDataStream
    from ...content.pricing.chain._stream import StreamingChain
    from ...content._universe_streams import _UniverseStreams
    from . import OMMStream, RDPStream

    Stream = Union[
        _UniverseStreams,
        StreamingChain,
        TradeDataStream,
        RDPStream,
        OMMStream,
        QuantitativeDataStream,
    ]

stream_state_to_open_state = {
    StreamState.Opened: OpenState.Opened,
    StreamState.Opening: OpenState.Pending,
    StreamState.Closed: OpenState.Closed,
    StreamState.Closing: OpenState.Pending,
}


class StreamOpenMixin(AbstractContextManager, AbstractAsyncContextManager):
    _stream: "Stream" = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    async def __aenter__(self):
        await self.open_async()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def open_state(self) -> OpenState:
        return stream_state_to_open_state.get(self._stream.state)

    def open(self) -> OpenState:
        self._stream.open()
        return self.open_state

    async def open_async(self) -> OpenState:
        await self._stream.open_async()
        return self.open_state

    def close(self) -> OpenState:
        self._stream.close()
        return self.open_state


class StreamOpenWithUpdatesMixin(StreamOpenMixin):
    def open(self, with_updates: bool = True) -> OpenState:
        self._stream.open(with_updates=with_updates)
        return self.open_state

    async def open_async(self, with_updates: bool = True) -> OpenState:
        await self._stream.open_async(with_updates=with_updates)
        return self.open_state
