import re
from collections import Counter
from datetime import date, datetime, timedelta
from itertools import groupby, zip_longest
from logging import Logger
from typing import Dict, List, Optional, Union, Tuple, Sequence

import pandas as pd
from dateutil.parser import parse
from pandas import DataFrame

from .._core import session
from .._tools import (
    ADC_FUNC_PATTERN_IN_FIELDS,
    ADC_TR_PATTERN,
    DEBUG,
    fields_arg_parser,
    fr_datetime_adapter,
    ohlc,
    universe_arg_parser,
)
from ..content import custom_instruments, fundamental_and_reference, historical_pricing
from ..content._df_builder import (
    process_historical_raw,
    dfbuilder_udf,
    dfbuilder_rdp,
)
from ..content.fundamental_and_reference._data_grid_type import (
    DataGridType,
    get_data_grid_type,
)
from ..content.fundamental_and_reference._definition import determine_content_type
from ..content.historical_pricing._hp_data_provider import EventTypes

EVENTS_INTERVALS = {
    "tick": {"event_types": None, "adc": "D"},
    "tas": {"event_types": EventTypes.TRADE, "adc": "D"},
    "taq": {"event_types": EventTypes.QUOTE, "adc": "D"},
}

INTERVALS = {
    **EVENTS_INTERVALS,
    "minute": {"pricing": "PT1M", "adc": "D"},
    "1min": {"pricing": "PT1M", "adc": "D"},
    "5min": {"pricing": "PT5M", "adc": "D"},
    "10min": {"pricing": "PT10M", "adc": "D"},
    "30min": {"pricing": "PT30M", "adc": "D"},
    "60min": {"pricing": "PT60M", "adc": "D"},
    "hourly": {"pricing": "PT1H", "adc": "D"},
    "1h": {"pricing": "PT1H", "adc": "D"},
    "daily": {"pricing": "P1D", "adc": "D"},
    "1d": {"pricing": "P1D", "adc": "D"},
    "1D": {"pricing": "P1D", "adc": "D"},
    "7D": {"pricing": "P7D", "adc": "W"},
    "7d": {"pricing": "P7D", "adc": "W"},
    "weekly": {"pricing": "P1W", "adc": "W"},
    "1W": {"pricing": "P1W", "adc": "W"},
    "monthly": {"pricing": "P1M", "adc": "M"},
    "1M": {"pricing": "P1M", "adc": "M"},
    "quarterly": {"pricing": "P3M", "adc": "CQ"},
    "3M": {"pricing": "P3M", "adc": "CQ"},
    "6M": {"pricing": "P6M", "adc": "CS"},
    "yearly": {"pricing": "P1Y", "adc": "CY"},
    "12M": {"pricing": "P1Y", "adc": "CY"},
    "1Y": {"pricing": "P1Y", "adc": "CY"},
}

NON_INTRA_DAY_INTERVALS = {
    "daily",
    "1d",
    "1D",
    "weekly",
    "7D",
    "7d",
    "1W",
    "monthly",
    "1M",
    "quarterly",
    "3M",
    "yearly",
    "1Y",
}


def get_history(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    interval: Optional[str] = None,
    start: Union[str, date, datetime, timedelta] = None,
    end: Union[str, date, datetime, timedelta] = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
    use_field_names_in_headers: Optional[bool] = False,
) -> DataFrame:
    """
    With this tool you can request historical data from Pricing and ADC

    Parameters
    ----------
        universe: str | list
            instruments to request.
        fields: str | list, optional
            fields to request.
        interval: str, optional
            The consolidation interval. Supported intervals are:
            tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
            1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
        start: str or date or datetime or timedelta, optional
            The start date and timestamp of the query in ISO8601 with UTC only
        end: str or date or datetime or timedelta, optional
            The end date and timestamp of the query in ISO8601 with UTC only
        adjustments : str, optional
            The adjustment
        count : int, optional
            The maximum number of data returned. Values range: 1 - 10000
        use_field_names_in_headers : bool, optional
            Return field name in headers instead of title

    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """
    if interval is not None and interval not in INTERVALS:
        raise ValueError(
            f"Not supported interval value.\nSupported intervals are:"
            f"{list(INTERVALS.keys())}"
        )

    content_type = determine_content_type(session.get_default())
    platform = get_data_grid_type(content_type)
    if platform == DataGridType.UDF:
        dfbuilder = dfbuilder_udf
    elif platform == DataGridType.RDP:
        dfbuilder = dfbuilder_rdp

    universe = universe_arg_parser.get_list(universe)
    fields = fields_arg_parser.get_list(fields or [])
    logger = session.get_default().logger()

    # adc and historical pricing
    adc_universe = tuple(inst for inst in universe if not inst.startswith("S)"))
    adc_fields = get_adc_fields(fields)
    hp_fields = [field for field in fields if field not in adc_fields]
    cusinst_universe = [inst for inst in universe if inst.startswith("S)")]

    adc_raw, hp_raw, custom_inst_data, adc_df, hp_df, custom_inst_df = [None] * 6

    # adc
    if adc_universe:
        adc_params = get_adc_params(start, end, interval)
        adc_raw, adc_df = get_adc_data(
            universe=adc_universe,
            fields=adc_fields,
            parameters=adc_params,
            use_field_names_in_headers=use_field_names_in_headers,
            logger=logger,
        )

    if adc_raw:
        adc_raw_rics = tuple(x[0] for x in adc_raw["data"])
        hp_universe = adc_raw_rics or adc_universe
    else:
        hp_universe = adc_universe

    # Historical pricing
    if not fields or hp_fields:
        hp_raw, hp_df = get_hp_data(
            universe=hp_universe,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=hp_fields,
            logger=logger,
        )

    # custom_instruments
    if cusinst_universe:
        custom_inst_data, custom_inst_df = get_custominsts_data(
            universe=cusinst_universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
            logger=logger,
        )

    if adc_raw and fields:
        adc_fields_set = set(adc_fields)
        fields_set = set(fields)
        if adc_fields_set.isdisjoint(fields_set):
            adc_raw = None

    if not any([adc_raw, hp_raw, custom_inst_data]):
        df = DataFrame()
        return df

    if adc_raw and not (hp_raw or custom_inst_data):
        if not is_raw_headers_in_fields(adc_raw, fields, platform):
            adc_df = DataFrame()
        if len(adc_fields) == 1 and len(adc_universe) > 1 and not hp_fields:
            df_cols = [i for i in adc_df.columns]
            first_col = set.intersection(*map(set, df_cols))
            adc_df = adc_df.droplevel(level=1, axis=1)
            adc_df.rename_axis(columns=list(first_col), inplace=True)
        adc_df.sort_index(ascending=True, inplace=True)
        adc_df.ohlc = ohlc.__get__(adc_df, None)
        return adc_df

    if hp_raw and not (adc_raw or custom_inst_data):
        hp_df.ohlc = ohlc.__get__(hp_df, None)
        return hp_df

    if custom_inst_data and not (adc_raw or hp_raw):
        custom_inst_df.ohlc = ohlc.__get__(custom_inst_df, None)
        return custom_inst_df

    adc_data, universes = prepare_adc_data_and_universes(
        adc_raw, adc_universe, adc_fields, interval, platform, dfbuilder
    )
    hp_data, raw_fields = prepare_hp_data(
        hp_raw, hp_universe, hp_fields, interval, platform
    )

    # for cases when request looks like rd.get_history(universe="LSEG.L")
    if not (fields and hp_fields) and adc_fields == ["TR.RIC"]:
        fields = raw_fields

    if not fields:
        fields = get_hp_fields(hp_raw)

    data = prepare_data(adc_data, hp_data, universes, fields, platform)

    if platform == DataGridType.UDF:
        headers = prepare_udf_headers(adc_raw, fields)
    elif platform == DataGridType.RDP:
        headers = prepare_rdp_headers(adc_raw, fields)

    df = dfbuilder.build_date_as_index(
        {"data": data, "headers": headers}, use_field_names_in_headers
    )
    if len(universes) > 1:
        df.rename(columns={k: v for k, v in enumerate(universes)}, inplace=True)

    if cusinst_universe and custom_inst_data:
        custom_inst_data = prepare_custominsts_data(
            custom_inst_data, cusinst_universe, hp_fields, platform
        )
        cust_headers = prepare_custominst_headers(hp_fields, platform)
        cust_df = dfbuilder.build_date_as_index(
            {"data": custom_inst_data, "headers": cust_headers},
            use_field_names_in_headers,
            use_multiindex=True,
        )
        df = pd.concat([df, cust_df], axis=1)
        df.fillna(pd.NA, inplace=True)

    if interval is not None and interval not in NON_INTRA_DAY_INTERVALS:
        df.index.names = ["Timestamp"]
    df.sort_index(ascending=True, inplace=True)
    df.ohlc = ohlc.__get__(df, None)

    return df


def get_hp_data(
    universe: Sequence[str],
    fields: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    adjustments: Optional[str],
    count: Optional[int],
    logger: Logger,
):
    """Get historical pricing raw data.

    Args:
        universe (Sequence[str]): Sequence of RICs.
        fields (List[str]): List of fields for request.
        interval (Optional[str]): consolidation interval.
        start (Optional[str]): start date.
        end (Optional[str]): end date.
        adjustments (Optional[str]): adjustments for request.
        count (Optional[int]): the maximum number of data returned.
        logger (Logger): session logger.
    """
    if interval in EVENTS_INTERVALS:
        definition = historical_pricing.events.Definition(
            universe=list(universe),
            eventTypes=INTERVALS[interval]["event_types"],
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval

        definition = historical_pricing.summaries.Definition(
            universe=list(universe),
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    try:
        response = definition.get_data()
        DEBUG and logger.debug(
            f"HISTORICAL_PRICING --->\n{response.data.df.to_string()}\n"
        )
        raw = response.data.raw
        df = response.data.df
        return raw, df
    except Exception:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}")
        df = DataFrame()
        return None, df


def get_adc_params(
    start: Union[str, date, datetime, timedelta],
    end: Union[str, date, datetime, timedelta],
    interval: Optional[str],
) -> dict:
    """Get parameters for ADC request.

    Args:
        start: start date for calculation parameters.
        end: end date for calculation parameters.
        interval: consolidated interval for calculation parameters.

    Returns:
        parameters: parameters for ADC request.
    """
    parameters = {}
    if start is not None:
        parameters["SDate"] = fr_datetime_adapter.get_str(start)

    if end is not None:
        parameters["EDate"] = fr_datetime_adapter.get_str(end)

    if interval is not None:
        parameters["FRQ"] = INTERVALS[interval]["adc"]

    return parameters


def get_adc_data(
    universe: Sequence[str],
    fields: List[str],
    parameters: dict,
    use_field_names_in_headers: bool,
    logger: Logger,
) -> Union[Tuple[dict, DataFrame], Tuple[None, DataFrame]]:
    """Get ADC raw data.

    Args:
        universe (Sequence[str]): sequence of RICs.
        fields (List[str]): list of fields for request.
        parameters (Dict[str]): precalculated parameters for request.
        use_field_names_in_headers (bool): return fields names in headers instead of title.
        logger (Logger): session logger.
    """
    definition = fundamental_and_reference.Definition(
        universe=list(universe),
        fields=fields,
        parameters=parameters,
        row_headers="date",
        use_field_names_in_headers=use_field_names_in_headers,
    )
    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"ADC --->\n{response.data.df.to_string()}\n")
        return raw, df
    except Exception:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}")
        return None, DataFrame()


def get_custominsts_data(
    universe: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    count: Optional[int],
    logger: Logger,
) -> Union[Tuple[dict, DataFrame], Tuple[None, DataFrame]]:
    """Get custom instruments raw data.

    Args:
        universe (List[str]): list of RICs.
        interval (Optional[str]): optional interval.
        start (Optional[str]): optional start date.
        end (Optional[str]): optional end date.
        count (OptDict[int]): maximim number of retrieved data.
        logger (Logger): session logger.
    """
    if interval in EVENTS_INTERVALS:
        definition = custom_instruments.events.Definition(
            universe=universe,
            start=start,
            end=end,
            count=count,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval
        definition = custom_instruments.summaries.Definition(
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
        )

    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"CUSTOMINSTS --->\n{response.data.df.to_string()}\n")
        return raw, df
    except Exception:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}")
        return None, DataFrame()


def get_adc_fields(fields: List[str]) -> List[str]:
    """Get ADC fields for request.

    Args:
        fields (List[str]): list of fields to filter.

    Returns:
        adc_fields (List[str]): list of adc_fields.
    """
    adc_tr_fields = [field for field in fields if re.match(ADC_TR_PATTERN, field)]
    adc_funcs_in_fields = [
        field for field in fields if re.match(ADC_FUNC_PATTERN_IN_FIELDS, field)
    ]
    adc_fields = adc_tr_fields + adc_funcs_in_fields

    if not adc_fields:
        adc_fields = ["TR.RIC"]

    return adc_fields


def is_raw_headers_in_fields(adc_raw, fields, platform):
    fields = {field.casefold() for field in fields}
    adc_headers = set()
    if platform == DataGridType.RDP:
        for header in adc_raw["headers"]:
            if (
                header["name"] not in ["instrument", "date"]
                and ")" not in header["name"]
            ):
                if " " in header["title"]:
                    adc_headers.add(header["name"].casefold())
                elif header["name"] == "RIC" and header["title"] == "RIC":
                    adc_headers.add("tr.ric")
                else:
                    if header["name"].split(".")[-1] == header["title"]:
                        adc_headers.add(header["name"].casefold())
                    else:
                        adc_headers.add(
                            f"{header['name'].casefold()}.{header['title'].casefold()}"
                        )
    elif platform == DataGridType.UDF:
        for header in adc_raw["headers"][0]:
            if header.get("field"):
                adc_headers.add(header.get("field").casefold())

    return adc_headers.issubset(fields)


def group_universes(universes: Sequence[str]):
    get_valid_universe = (
        i if not (i.startswith("0#.") or i.startswith("Peers(")) else ""
        for i in universes
    )
    group_universe = groupby(get_valid_universe)
    return [
        (name, len([_ for _ in items])) for name, items in group_universe if name != ""
    ]


def chunks(generator, chunk_size):
    """Yield successive chunks from a generator"""
    chunk = []

    for item in generator:
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = [item]
        else:
            chunk.append(item)

    if chunk:
        yield chunk


def prepare_adc_data_and_universes(
    adc_raw, adc_universe, adc_fields, interval, platform, dfbuilder
) -> Tuple[List[list], List[str]]:
    """Transform adc data to further merging.

    Transformed data looks like:
        {
            "RIC": [{"Date": "value", "field": "value", "another_field": "value"}],
            "NEXT_RIC": [{"Date": "value", "field": "value", "next_field": "value"}]
        }
    """
    headers = dfbuilder.get_headers(adc_raw)

    cols = []
    if platform == DataGridType.UDF:
        cols = [col["name"] for col in headers if col["name"] != "Instrument"]
        date_name = "Date"
    elif platform == DataGridType.RDP:
        for header in headers:
            header_str = f"{header['name']}.{header['title']}".casefold()
            header_name = header["name"].casefold()
            fields = [field.casefold() for field in adc_fields]
            if header_name == "instrument":
                continue
            elif header_str in fields:
                cols.append(f"{header['name']}.{header['title']}")
            else:
                cols.append(header["name"])

        date_name = "date"

    adc_cols = ["Type", *cols]

    adc_data = []
    new_universes = []
    index_universe = 0
    group_data = groupby(adc_raw["data"], lambda x: x[0])
    group_universes_count = group_universes(adc_universe)
    counter_items = Counter()

    for ric, items in group_data:
        items = [i for i in items]
        len_items = len(items)
        counter_items.update([len_items])
        result_items = []

        if index_universe < len(group_universes_count):
            name_universe, count = group_universes_count[index_universe]
        else:
            count = 0
            name_universe = ""

        for item in items:
            item[0] = "adc"
            item = {k: v for k, v in zip(adc_cols, item)}
            item_date_name = item.get(date_name)
            if interval in NON_INTRA_DAY_INTERVALS and item_date_name:
                item[date_name] = item_date_name.split("T")[0]
            elif item_date_name:
                item[date_name] = item_date_name.replace("T", " ").replace("Z", "")
            result_items.append(item)

        repeat_universe = 1
        if ric == name_universe:
            if count == len_items:
                repeat_universe = count
                for i in result_items:
                    adc_data.append([i])
            elif (
                count < len_items
                and counter_items.most_common(1)[0][0] * (count + 1) == len_items
            ):
                repeat_universe = count + 1
                for chunk in chunks(result_items, len_items // repeat_universe):
                    adc_data.append(chunk)
            elif count < len_items:
                repeat_universe = count
                for chunk in chunks(result_items, len_items // count):
                    adc_data.append(chunk)
            elif count > len_items:
                for chunk in chunks(result_items, len_items):
                    adc_data.append(chunk)
            index_universe += 1
        else:
            adc_data.append(result_items)

        new_universes.extend([ric] * repeat_universe)

    return adc_data, new_universes


def prepare_hp_data(hp_raw, adc_and_hp_universe, hp_fields, interval, platform):
    """Transform historical pricing data to further merging.

    Transformed data looks like:
        {
            "RIC": [{"Date": "value", "field": "value", "another_field": "value"}],
            "NEXT_RIC": [{"Date": "value", "field": "value", "next_field": "value"}]
        }
    """
    hp_data = tuple([] for _ in adc_and_hp_universe)
    if platform == DataGridType.UDF:
        date_name = "Date"
    elif platform == DataGridType.RDP:
        date_name = "date"

    if isinstance(hp_raw, dict):
        raw_datas, raw_columns, raw_dates = process_historical_raw(hp_raw, hp_fields)
        for raw_data, raw_date in zip(raw_datas, raw_dates):
            if interval in NON_INTRA_DAY_INTERVALS:
                hp_data_item = {
                    "Type": "pricing",
                    date_name: str(raw_date).split(" ")[0],
                }
            else:
                hp_data_item = {"Type": "pricing", date_name: str(raw_date)}

            if hp_fields:
                hp_data_item.update((item for item in zip(hp_fields, raw_data)))
            else:
                hp_data_item.update((item for item in zip(raw_columns, raw_data)))
            hp_data[0].append(hp_data_item)

        if not hp_fields:
            hp_fields = raw_columns

    elif isinstance(hp_raw, list):
        for index, item in enumerate(hp_raw):
            if isinstance(item, list):
                hp_data[index].append({"Type": "pricing", date_name: None})
            else:
                if not hp_fields:
                    hp_fields = [header["name"] for header in item["headers"]]
                raw_datas, _, raw_dates = process_historical_raw(item, hp_fields)
                for raw_data, raw_date in zip(raw_datas, raw_dates):
                    if interval in NON_INTRA_DAY_INTERVALS:
                        hp_data_item = {
                            "Type": "pricing",
                            date_name: str(raw_date).split(" ")[0],
                        }
                    else:
                        hp_data_item = {"Type": "pricing", date_name: str(raw_date)}

                    hp_data_item.update((item for item in zip(hp_fields, raw_data)))
                    hp_data[index].append(hp_data_item)

    return hp_data, hp_fields


def get_hp_fields(raw_data):
    hp_fields = []

    if isinstance(raw_data, dict):
        hp_fields = [header["name"] for header in raw_data["headers"]]
    if isinstance(raw_data, list):
        for item in raw_data:
            hp_raw_fields = [header["name"] for header in item["headers"]]
            if hp_raw_fields != hp_fields:
                hp_fields = hp_raw_fields

    return hp_fields


def prepare_custominst_headers(hp_data, platform):
    headers = []
    if platform == DataGridType.UDF:
        headers.append([{"displayName": "Instrument"}, {"displayName": "Date"}])
        for item in hp_data:
            headers[0].append({"displayName": item, "field": item})
    elif platform == DataGridType.RDP:
        headers.extend(
            [
                {"name": "instrument", "title": "Instrument"},
                {"name": "date", "title": "Date"},
            ]
        )
        for item in hp_data:
            headers.append({"name": item, "title": item})
    return headers


def prepare_custominsts_data(custominsts_raw, cust_rics, hp_fields, platform):
    if platform == DataGridType.UDF:
        idx_map = {"Instrument": 0, "Date": 1}
    elif platform == DataGridType.RDP:
        idx_map = {"instrument": 0, "date": 1}

    col_idx = {item: hp_fields.index(item) + 2 for item in hp_fields}
    idx_map.update(col_idx)

    result = []

    if isinstance(custominsts_raw, dict):
        ric = custominsts_raw["universe"]["ric"]
        if platform == DataGridType.UDF:
            cust_headers = [
                item["name"].capitalize() if item["name"] == "DATE" else item["name"]
                for item in custominsts_raw["headers"]
            ]
        elif platform == DataGridType.RDP:
            cust_headers = [
                item["name"].lower() if item["name"] == "DATE" else item["name"]
                for item in custominsts_raw["headers"]
            ]

        for item in custominsts_raw["data"]:
            processed_item = []

            if platform == DataGridType.UDF:
                raw_res = {"Instrument": ric}
                raw_res.update({k: v for k, v in zip(cust_headers, item)})
                for i in idx_map.keys():
                    processed_item.insert(idx_map[i], raw_res.get(i))

            elif platform == DataGridType.RDP:
                raw_res = {"instrument": ric}
                for key, value in zip(cust_headers, item):
                    try:
                        parse(value, fuzzy=False)
                        value = f"{value} 00:00:00"
                        raw_res.update({key: value})
                    except (ValueError, TypeError):
                        raw_res.update({key: value})

                for i in idx_map.keys():
                    processed_item.insert(idx_map[i], raw_res.get(i))

            result.append(processed_item)
    elif isinstance(custominsts_raw, list):
        for data_item in custominsts_raw:
            if not data_item:
                continue
            ric = data_item["universe"]["ric"]
            if platform == DataGridType.UDF:
                cust_headers = [
                    item["name"].capitalize()
                    if item["name"] == "DATE"
                    else item["name"]
                    for item in data_item["headers"]
                ]
            elif platform == DataGridType.RDP:
                cust_headers = [
                    item["name"].lower() if item["name"] == "DATE" else item["name"]
                    for item in data_item["headers"]
                ]
            for item in data_item["data"]:
                processed_item = []

                if platform == DataGridType.UDF:
                    raw_res = {"Instrument": ric}
                    raw_res.update({k: v for k, v in zip(cust_headers, item)})
                    for i in idx_map.keys():
                        processed_item.insert(idx_map[i], raw_res.get(i))

                elif platform == DataGridType.RDP:
                    raw_res = {"instrument": ric}
                    for key, value in zip(cust_headers, item):
                        try:
                            parse(value, fuzzy=False)
                            value = f"{value} 00:00:00"
                            raw_res.update({key: value})
                        except (ValueError, TypeError):
                            raw_res.update({key: value})

                    for i in idx_map.keys():
                        processed_item.insert(idx_map[i], raw_res.get(i))

                result.append(processed_item)

    return result


def prepare_udf_headers(adc_raw: dict, fields: List[str]) -> List[List[str]]:
    """Prepare headers to pass them to df_builder.

    Args:
        adc_raw (dict): adc raw data from adc response.
        fields (List[str]): fields requested by user.

    Returns:
        List with inserted list of dicts that describe each header in understandable
        by df builder format.
    """
    col_idx = {item.upper(): fields.index(item) + 2 for item in fields}
    result = [{"displayName": "Instrument"}, {"displayName": "Date"}]

    headers = adc_raw["headers"][0]
    for header in headers:
        if len(header) > 1:
            if header["field"].upper() not in list(col_idx.keys()):
                continue
            result.insert(col_idx[header["field"].upper()], header)
            col_idx.pop(header["field"].upper())
    for name, index in col_idx.items():
        result.insert(index, {"displayName": name, "field": name})
    return [result]


def prepare_rdp_headers(adc_raw, fields):
    columns_index = {item.casefold(): fields.index(item) + 2 for item in fields}

    result = [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
    ]

    headers = adc_raw["headers"]

    for header in headers:
        header_str = f"{header['name']}.{header['title']}".casefold()
        header_name = header["name"].casefold()
        index_keys = list(columns_index.keys())

        if header_name in index_keys and header_str not in index_keys:
            result.insert(columns_index[header_name], header)
            columns_index.pop(header_name)

        if header_str in index_keys:
            result.insert(columns_index[header_str], header)
            columns_index.pop(header_str)

    for name, index in columns_index.items():
        result.insert(index, {"name": name.upper(), "title": name.upper()})

    return result


def prepare_data(
    adc_data: List[list],
    hp_data: Sequence[list],
    instruments: Sequence[str],
    columns: List[str],
    platform: DataGridType,
) -> List[list]:
    prepared_data = []

    if platform == DataGridType.UDF:
        date_name = "Date"
    elif platform == DataGridType.RDP:
        date_name = "date"

    # Have to add +2 to index because first two items will be instrument and date
    # see _df_builder.DFBuilder.build_date_as_index
    idx_map = {"Date": 1}
    cols = [item.upper() if item.startswith("TR") else item for item in columns]
    col_idx = {item: cols.index(item) + 2 for item in cols}
    idx_map.update(col_idx)

    flag_instruments = len(instruments) == 1

    for index, instrument in enumerate(instruments):
        adc = adc_data[index] if index < len(adc_data) else []
        hp = hp_data[index] if index < len(hp_data) else []
        data = [*adc, *hp]

        unique_dates = list(dict.fromkeys([item[date_name] for item in data]))
        keys = idx_map.keys()
        for date_item in unique_dates:
            sorted_by_date_items = [
                item for item in data if item[date_name] == date_item
            ]
            res = {}
            group_items = groupby(sorted_by_date_items, lambda item: item["Type"])
            for item_type, items in group_items:
                items = [item for item in items]
                res[item_type] = items
            if len(res) == 1:
                result_values = next(iter(res.values()))
                for i in result_values:
                    result = [instrument] if flag_instruments else [index]
                    i_keys = {key.casefold(): key for key in i.keys()}
                    for key in keys:
                        if key.casefold() in list(i_keys.keys()):
                            result.insert(idx_map[key], i.get(i_keys[key.casefold()]))
                        else:
                            result.insert(idx_map[key], None)
                    prepared_data.append(result)
            else:
                vals = list(res.values())
                vals_list = [sorted(item, key=lambda d: d[date_name]) for item in vals]
                for one, two in zip_longest(*vals_list, fillvalue=None):
                    result = [instrument] if flag_instruments else [index]
                    if all([one, two]):
                        item = {**one, **two}
                        i_keys = {key.casefold(): key for key in item.keys()}
                        for key in keys:
                            if key.casefold() in list(i_keys.keys()):
                                result.insert(
                                    idx_map[key], item.get(i_keys[key.casefold()])
                                )
                            else:
                                result.insert(idx_map[key], None)
                    else:
                        item = one or two
                        i_keys = {key.casefold(): key for key in item.keys()}
                        for key in keys:
                            if key.casefold() in list(i_keys.keys()):
                                result.insert(
                                    idx_map[key], item.get(i_keys[key.casefold()])
                                )
                            else:
                                result.insert(idx_map[key], None)
                    prepared_data.append(result)
    return prepared_data
