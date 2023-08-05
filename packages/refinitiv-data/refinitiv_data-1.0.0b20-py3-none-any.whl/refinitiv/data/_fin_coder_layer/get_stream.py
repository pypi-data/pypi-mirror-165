from contextlib import AbstractContextManager
from typing import Callable, List, Optional, Union, TYPE_CHECKING

import pandas as pd

from ._mixed_streams import Stream
from ._pricing_recorder import PricingRecorder
from .get_data import _send_request
from .._core.session import get_default
from .._tools import cached_property, custom_insts_historical_universe_parser
from ..content import fundamental_and_reference
from ..content._universe_stream import _UniverseStream

if TYPE_CHECKING:
    from .. import OpenState


def make_callback(on_data, logger):
    def callback(update, ric, stream):
        try:
            stream = PricingStream(stream)
            df = pd.DataFrame(update, index=[ric])
            on_data(df, ric, stream)
        except Exception as error:
            logger.error(error)

    return callback


def open_pricing_stream(
    universe: Union[str, List[str]],
    fields: Union[str, List[str]] = None,
    service: Optional[str] = None,
    on_data: Optional[Callable] = None,
) -> "PricingStream":
    """
    Create and open pricing stream

    Parameters
    ----------

    universe : str or list of str
        The single/multiple instrument/s name (e.g. "EUR=" or ["EUR=", "CAD=", "UAH="])
    fields : list, str, optional
        Specifies the specific fields to be delivered when messages arrive
    service : str, optional
        Name of the streaming service publishing the instruments
    on_data : function, optional
        Callback function for on_update and on_refresh events

    Returns
    ----------
    PricingStream

    Examples
    -------
    Create pricing stream

    >>> import refinitiv.data as rd
    >>> def callback(updated_data, ric, stream):
    ...    print(updated_data)
    >>> pricing_stream = rd.open_pricing_stream(universe=['EUR='], fields=['BID', 'ASK', 'OPEN_PRC'], on_data=callback)  # noqa
    """
    logger = get_default().logger()
    universe = custom_insts_historical_universe_parser.get_list(universe)
    custom_insts_universe = [i for i in universe if i.startswith("S)")]
    pricing_universe = [i for i in universe if i not in custom_insts_universe]
    if pricing_universe:
        _adc_df = _send_request(
            data_provider=fundamental_and_reference.Definition,
            params={"universe": pricing_universe, "fields": ["TR.RIC"]},
            logger=logger,
        )

        pricing_universe = list(_adc_df.get("Instrument", pricing_universe))
    universe = pricing_universe + custom_insts_universe
    _stream = Stream(universe=universe, fields=fields, service=service)

    if on_data:
        _stream.on_update(make_callback(on_data, logger))
        _stream.on_refresh(make_callback(on_data, logger))
    stream = PricingStream(_stream)

    stream.open()
    return stream


class PricingStream(AbstractContextManager):
    def __init__(self, stream):
        self._stream = stream

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self, with_updates: bool = True) -> "OpenState":
        return self._stream.open(with_updates=with_updates)

    def close(self) -> "OpenState":
        return self._stream.close()

    def get_snapshot(
        self,
        universe: Union[str, List[str], None] = None,
        fields: Optional[List[str]] = None,
        convert: bool = True,
    ) -> "pd.DataFrame":
        return self._stream.get_snapshot(
            universe=universe, fields=fields, convert=convert
        )

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        return self._stream._get_fields(universe=universe, fields=fields)

    def __getitem__(self, item) -> "_UniverseStream":
        return self._stream.__getitem__(item)

    def __iter__(self):
        return self._stream.__iter__()

    @cached_property
    def recorder(self) -> PricingRecorder:
        return PricingRecorder(self._stream._stream)
