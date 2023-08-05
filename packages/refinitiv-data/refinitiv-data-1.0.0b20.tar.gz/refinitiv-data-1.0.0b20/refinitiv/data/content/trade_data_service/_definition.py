from typing import TYPE_CHECKING

from ._stream_facade import Stream
from .._types import OptList, OptDict
from ..._tools import create_repr

from ._stream import Events, FinalizedOrders, UniverseTypes

if TYPE_CHECKING:
    from ..._core.session import Session


class Definition:
    """
    This class describes Analytics Trade Data Service.

    Parameters
    ----------
    universe : list, optional
        A list of RIC or symbol or user's id for retrieving trading analytics data.
    fields : list, optional
        A list of enumerate fields.
    events : Events, optional
        Enable/Disable the detail of order event in the streaming.
        Default: False
    finalized_orders : FinalizedOrders, optional
        Enable/Disable the cached of finalized order of current day in the streaming.
        Default: False
    filters : list, optional
        Set the condition of subset of trading streaming data.
    universe_type : UniverseTypes, optional
        A type of given universe can be RIC, Symbol or UserID.
        Default: UniverseTypes.RIC
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    get_stream(session=session)
        Get stream object of this definition

    Examples
    --------
    >>> from refinitiv.data.content import trade_data_service
    >>> definition = trade_data_service.Definition()
    """

    def __init__(
        self,
        universe: OptList = None,
        universe_type: UniverseTypes = UniverseTypes.UserID,
        fields: OptList = None,
        events: Events = Events.No,
        finalized_orders: FinalizedOrders = FinalizedOrders.No,
        filters: OptList = None,
        extended_params: OptDict = None,
    ):
        self._universe = universe
        self._universe_type = universe_type
        self._fields = fields
        self._events = events
        self._finalized_orders = finalized_orders
        self._filters = filters
        self._extended_params = extended_params

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.trade_data_service",
            content={"universe": self._universe},
        )

    def get_stream(self, session: "Session" = None) -> Stream:
        """
        Returns a streaming trading analytics subscription.

        Parameters
        ----------
        session : Session, optional
            The Session used by the TradeDataService to retrieve data from the platform

        Returns
        -------
        TradeDataStream

        Examples
        --------
        >>> from refinitiv.data.content import trade_data_service
        >>> definition = trade_data_service.Definition()
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        stream = Stream(
            session=session,
            universe=self._universe,
            universe_type=self._universe_type,
            fields=self._fields,
            events=self._events,
            finalized_orders=self._finalized_orders,
            filters=self._filters,
            extended_params=self._extended_params,
        )
        return stream
