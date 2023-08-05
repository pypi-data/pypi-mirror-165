import re
import sys
from collections import Counter
from typing import Callable, TYPE_CHECKING, Union

import numpy as np
import pandas as pd
from pandas import DataFrame

from .._core.session import get_default, is_open
from .._tools import (
    DEBUG,
    custom_insts_historical_universe_parser,
    fields_arg_parser,
)
from .._tools._dataframe import convert_df_columns_to_datetime
from ..content import fundamental_and_reference
from ..errors import RDError

NOT_ALLOWED_SNAPSHOT_FIELDS = {"Date"}
# re for ADC fields like started with "TR." case is ignored

ADC_TR_PATTERN = re.compile(r"^tr\..+", re.I)

# re for ADC functions in fields like AVAIL(, AVG(
# AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum))

ADC_FUNC_PATTERN_IN_FIELDS = re.compile(r"^[A-Z]+\(")

if TYPE_CHECKING:
    from logging import Logger


def get_log_string(fields, universe):
    return f"Fields: {fields} for {universe}"


def _send_request(
    data_provider: Callable,
    params: dict,
    logger: "Logger",
    default_df: DataFrame = DataFrame(),
) -> DataFrame:
    fields = params.get("fields", "")
    universe = params["universe"]
    logger.info(f"Requesting {get_log_string(fields, universe)} \n")
    df = default_df

    try:
        response = data_provider(**params).get_data()
    except RDError as e:
        logger.debug(f"Failure response into content layer: {str(e)}")
        df.flags.exception_event = {"raise_exception": False, "exception": None}
    except Exception as e:
        if DEBUG:
            raise e
        logger.exception(f"Failure sending request with {data_provider}")
        df.flags.exception_event = {
            "raise_exception": True,
            "exception": sys.exc_info()[:2],
        }
    else:
        request_messages = response.request_message
        statuses = response.http_status
        if not isinstance(response.request_message, list):
            request_messages = [response.request_message]
            statuses = [response.http_status]

        for request, status in zip(request_messages, statuses):
            path = request.url.path
            cur_universe = path.rsplit("/", 1)[-1]
            if cur_universe not in universe:
                cur_universe = universe
            logger.info(
                f"Request to {path} with {get_log_string(fields, cur_universe)}\n"
                f"status: {status}\n"
            )

        # this check can be removed after all API would return
        # dataframe in response or raise exception
        try:
            df_ = response.data.df
        except Exception as e:
            logger.debug(f"Failure build df into content layer: {str(e)}")
            df_ = None

        if df_ is not None:
            df = df_
            df.flags.exception_event = {"raise_exception": False, "exception": None}
        else:
            df.flags.exception_event = {
                "raise_exception": False,
                "exception": response.http_status,
            }

    return df


def _rename_column_n_to_column(
    name: str, df: DataFrame, multiindex: bool = False, level: int = 1
) -> None:
    if multiindex:
        occurrences = (
            # fr"^{name}_\d+$" - searching columns like f"{name}_0", f"{name}_1"
            i
            for i in df.columns.levels[level]
            if re.match(rf"^{name}_\d+$", i)
        )
    else:
        occurrences = (i for i in df.columns if re.match(rf"^{name}_\d+$", i))

    df.rename(columns={i: name for i in occurrences}, inplace=True)


def _rename_column_to_column_n(name: str, df: DataFrame) -> None:
    new_names = []
    count = 0
    for i in df.columns:
        if i == name:
            if isinstance(i, tuple):
                column_name = i[1]
                column_name = f"{column_name}_{count}"
                i = (i[0], column_name)
            else:
                i = f"{i}_{count}"
            count += 1
        new_names.append(i)
    df.columns = new_names


def _find_and_rename_duplicated_columns(df: DataFrame) -> list:
    counted_columns = Counter(df.columns)
    duplicated_columns = [i for i, n in counted_columns.items() if n > 1]

    for i in duplicated_columns:
        _rename_column_to_column_n(i, df)

    return duplicated_columns


def show_requests_in_log(logger: "Logger", response: "Response", universe, fields):
    request_messages = response.request_message
    statuses = response.http_status
    if not isinstance(response.request_message, list):
        request_messages = [response.request_message]
        statuses = [response.http_status]

    for request, status in zip(request_messages, statuses):
        path = request.url.path
        cur_universe = path.rsplit("/", 1)[-1]
        if cur_universe not in universe:
            cur_universe = universe
        logger.info(
            f"Request to {path} with {get_log_string(fields, cur_universe)}\n"
            f"status: {status}\n"
        )


def get_adc_data(
    params: dict, logger: "Logger", dataframe=False
) -> Union[dict, "DataFrame"]:
    fields = params.get("fields", "")
    universe = params["universe"]
    logger.info(f"Requesting {get_log_string(fields, universe)} \n")
    definition = fundamental_and_reference.Definition(**params)

    try:
        response = definition.get_data()
        if dataframe:
            result = response.data.df
        else:
            result = response.data.raw
    except RDError as e:
        result = DataFrame() if dataframe else {}
        logger.debug(f"Failure response into content layer: {str(e)}")
    except Exception as e:
        if DEBUG:
            raise e
        result = DataFrame() if dataframe else {}
        logger.exception(f"Failure sending request with {definition}")
    else:
        show_requests_in_log(logger, response, universe, fields)
    return result


def merge_data(
    adc_columns: list, pricing_columns: list, adc_data: dict, pricing_data: dict
):
    columns = adc_columns + pricing_columns
    if not adc_columns and pricing_columns:
        columns.insert(0, "Instrument")

    data = adc_data
    result_data = []
    for universe in pricing_data:
        if universe in data:
            for column in data[universe]:
                column.extend(pricing_data[universe])
                result_data.append(column)
        else:
            data[universe] = (
                [universe] + [pd.NA] * (len(adc_columns) - 1) + pricing_data[universe]
            )
            result_data.append(data[universe])
    return columns, result_data


def get_columns_and_data_from_adc_raw(raw, use_field_names_in_headers):
    headers = raw.get("headers", [[{}]])
    if headers and isinstance(headers[0], list):
        columns = [
            header.get("displayName")
            if not use_field_names_in_headers
            else header.get("field", header.get("displayName"))
            for header in headers[0]
        ]
    else:
        columns = [
            header.get("name") if use_field_names_in_headers else header.get("title")
            for header in headers
        ]

        if "instrument" in columns:
            columns[columns.index("instrument")] = "Instrument"

    _data = raw.get("data", [])
    data = {}

    for column in _data:
        if column[0] not in data:
            data[column[0]] = []
        data[column[0]].append(convert_types(column, columns))
    if not data:
        columns = []
    return columns, data


def get_data_from_stream(universe, fields, logger, snapshot=False):
    from . import Stream

    logger.info(f"Requesting pricing info for fields={fields} via websocket\n")
    stream = Stream(universe=universe, fields=None)

    try:
        stream.open(with_updates=False)
        if not snapshot:
            result = get_columns_and_data_from_stream(stream, fields)
        else:
            result = stream.get_snapshot(fields=fields)
            if len(result.columns) == 1 or not any(
                [_stream.fields for _stream in stream]
            ):
                result = DataFrame()
        stream.close()

    except Exception:
        logger.debug(f"Failure retrieving data for {stream._stream.universe}")
        result = None, None if not snapshot else DataFrame()

    return result


def get_columns_from_stream(stream):
    columns = set()
    for _stream in stream:
        fields = _stream.fields or []
        columns.update(fields)
    return list(columns)


def get_columns_and_data_from_stream(stream, fields):
    stream_columns = get_columns_from_stream(stream)
    if fields:
        columns = [i for i in fields if i in stream_columns]
    else:
        columns = stream_columns
    data = {
        _stream.name: convert_types([_stream[column] for column in columns], columns)
        for _stream in stream
    }
    return columns, data


def convert_types(column, column_names):
    date_columns = [
        i
        for i, column_name in enumerate(column_names)
        if any([i for i in ["Date", "date", "_DT", "DATE"] if i in column_name])
        and all([i if i not in column_name else False for i in ["DateType", "Dates"]])
    ]
    result = [i if i is not None and i != "" else pd.NA for i in column]
    if date_columns:
        for i in date_columns:
            result[i] = pd.to_datetime(result[i])
    return result


def update_universe(raw, _universe):
    index = 0  # instrument
    data = raw.get("data")
    if data and all(isinstance(i[index], str) for i in data):
        universe = [i[index] for i in data]
    else:
        universe = _universe
    return universe


def get_data(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    parameters: Union[str, dict, None] = None,
    use_field_names_in_headers: bool = False,
) -> DataFrame:
    """
    With this tool you can request data from ADC, realtime pricing data or
    combination of both;

    Parameters
    ----------
        universe: str | list ,
            instruments to request.
        fields: str | list .
            fields to request.
        parameters: str | dict,
            Single global parameter key=value or dictionary
            of global parameters to request.
        use_field_names_in_headers: bool
            Return field name as column headers for data instead of title


    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_data(universe=['IBM.N', 'VOD.L'], fields=['BID', 'ASK'])
    >>> get_data(
    ...     universe=['GOOG.O', 'AAPL.O'],
    ...     fields=['TR.EV','TR.EVToSales'],
    ...     parameters = {'SDate': '0CY', 'Curn': 'CAD'}
    ...)
    >>> get_data(
    ...     universe=['IBM.N', 'VOD.L'],
    ...     fields=['BID', 'ASK', 'TR.Revenue'],
    ...     parameters = {'SCale':6, 'SDate':0, 'EDate':-3, 'FRQ':'FY'}
    ...)
    """
    session = get_default()
    logger = session.logger()
    if not is_open(session):
        error_message = "Session is not opened. Can't send any request"
        logger.error(error_message)
        raise ValueError(error_message)

    universe = custom_insts_historical_universe_parser.get_list(universe)
    fields = fields_arg_parser.get_list(fields) if fields else []

    adc_tr_fields = [i for i in fields if re.match(ADC_TR_PATTERN, i)]
    adc_funcs_in_fields = [i for i in fields if re.match(ADC_FUNC_PATTERN_IN_FIELDS, i)]
    adc_fields = adc_tr_fields + adc_funcs_in_fields
    pricing_fields = [i for i in fields if i not in adc_fields]

    custom_insts_universe = [i for i in universe if i.startswith("S)")]
    adc_and_pricing_universe = [i for i in universe if i not in custom_insts_universe]
    if not adc_and_pricing_universe:
        return get_data_from_stream(universe, pricing_fields, logger, snapshot=True)

    _fields = adc_fields or ["TR.RIC"]
    adc_params = dict(
        universe=adc_and_pricing_universe,
        fields=_fields,
        parameters=parameters,
        use_field_names_in_headers=use_field_names_in_headers,
    )
    pricing = bool(pricing_fields or not fields)
    adc = bool(adc_and_pricing_universe and adc_fields)

    # no data to return
    if not adc and not pricing:
        return DataFrame()

    # only adc data return
    if adc and not pricing:
        return get_adc_data(params=adc_params, logger=logger, dataframe=True)

    adc_raw = get_adc_data(params=adc_params, logger=logger)
    adc_and_pricing_universe = update_universe(adc_raw, adc_and_pricing_universe)
    universe = adc_and_pricing_universe + custom_insts_universe

    # update universe and only pricing data return
    if not adc:
        return get_data_from_stream(universe, pricing_fields, logger, snapshot=True)

    # merge_data
    pricing_columns, pricing_data = get_data_from_stream(
        universe, pricing_fields, logger
    )
    adc_columns, adc_data = get_columns_and_data_from_adc_raw(
        adc_raw, use_field_names_in_headers
    )
    columns, data = merge_data(adc_columns, pricing_columns, adc_data, pricing_data)
    if not any(columns):
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(np.array(data), columns=columns)
        df = convert_df_columns_to_datetime(
            df, pattern="Date", utc=True, delete_tz=True
        )
    return df
