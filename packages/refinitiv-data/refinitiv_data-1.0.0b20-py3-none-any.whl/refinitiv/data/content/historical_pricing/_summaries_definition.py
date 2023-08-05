from datetime import date, datetime, timedelta
from typing import Optional, Any, Union, List

from ._hp_data_provider import (
    get_content_type_by_interval,
    Adjustments,
    MarketSession,
)
from .._intervals import DayIntervalType, Intervals, get_day_interval_type
from ..._tools import hp_universe_parser, validate_types
from ...delivery._data._data_provider import DataProviderLayer, BaseResponse, Data


class Definition(DataProviderLayer[BaseResponse[Data]]):
    """
    Summary line of this class that defines parameters for requesting summaries from historical pricing

    Parameters
    ----------
    universe : str or list of str
        The entity universe
    interval : str or Intervals, optional
        The consolidation interval in ISO8601
    start : str or date or datetime or timedelta, optional
        The start date and timestamp of the query in ISO8601 with UTC only
    end : str or date or datetime or timedelta, optional
        The end date and timestamp of the query in ISO8601 with UTC only
    adjustments : list of Adjustments or Adjustments or str, optional
        The adjustment list or Adjustments type
    sessions : list of MarketSession or MarketSession or str, optional
        The list of market session classification or str
    count : int, optional
        The maximum number of data returned. Values range: 1 - 10000
    fields : list, optional
        The list of fields that are to be returned in the response
    closure : Any, optional
        Specifies the parameter that will be merged with the request
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.historical_pricing import summaries
    >>> definition_summaries = summaries.Definition("EUR")
    >>> response = definition_summaries.get_data()

    """

    def __init__(
        self,
        universe: Union[str, List[str]],
        interval: Union[str, Intervals] = None,
        start: Optional[Union[str, date, datetime, timedelta]] = None,
        end: Optional[Union[str, date, datetime, timedelta]] = None,
        adjustments: Union[List[Adjustments], Adjustments, str] = None,
        sessions: Union[List[MarketSession], MarketSession, str] = None,
        count: Optional[int] = None,
        fields: Optional[list] = None,
        closure: Optional[Any] = None,
        extended_params: Optional[dict] = None,
    ) -> None:
        # By default, if interval is not defined, interday default value is requested
        day_interval_type = get_day_interval_type(interval or DayIntervalType.INTER)
        content_type = get_content_type_by_interval(day_interval_type)
        universe = hp_universe_parser.get_list(universe)
        validate_types(count, [int, type(None)], "count")

        super().__init__(
            data_type=content_type,
            day_interval_type=day_interval_type,
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            sessions=sessions,
            count=count,
            fields=fields,
            closure=closure,
            extended_params=extended_params,
        )
