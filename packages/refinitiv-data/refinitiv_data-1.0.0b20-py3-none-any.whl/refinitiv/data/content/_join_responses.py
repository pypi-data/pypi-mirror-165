from functools import partial
from types import SimpleNamespace
from typing import List, Callable

import pandas as pd

from ._df_builder import historical_build_df_one_inst, historical_build_df_multi_inst
from ._types import Strings
from ..delivery._data._data_provider import Response, Data


def join_responses(
    responses: List[Response],
    join_dataframes: Callable = pd.concat,
    response_class=Response,
    data_class=Data,
    reset_index=False,
) -> Response:
    def build_df(*args, **kwargs):
        dfs = []
        df = None

        for response in responses:
            dfs.append(response.data.df)

        all_dfs_is_none = all(a is None for a in dfs)
        if not all_dfs_is_none:
            df = join_dataframes(dfs)

        if reset_index and df is not None:
            df = df.reset_index(drop=True)

        return df

    if len(responses) == 1:
        return responses[0]

    raws = []
    http_statuses = []
    http_headers = []
    request_messages = []
    http_responses = []
    errors = []
    is_successes = []

    for response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)
        is_successes.append(response.is_success)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.headers = http_headers
    raw_response.request = request_messages
    is_success = any(is_successes)
    response = response_class(raw_response=raw_response, is_success=is_success)
    response.data = data_class(raws, dfbuilder=build_df)
    response.errors += errors
    response.http_response = http_responses
    response._status = http_statuses

    return response


def get_first_success_response(responses: List[Response]) -> Response:
    successful = (response for response in responses if response.is_success)
    first_successful = next(successful, None)
    return first_successful


def join_historical_responses(
    responses: List[Response],
    universe: Strings,
    fields: Strings,
    axis_name: str,
) -> Response:
    if len(responses) == 1:
        response = responses[0]

        if not response.is_success:
            return response

        response.data = Data(
            response.data.raw,
            dfbuilder=partial(
                historical_build_df_one_inst,
                fields=fields,
                axis_name=axis_name,
            ),
        )
        return response

    raws = []
    errors = []
    http_statuses = []
    http_headers = []
    http_responses = []
    request_messages = []

    for response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.request = request_messages
    raw_response.headers = http_headers
    response = Response(raw_response=raw_response, is_success=True)
    response.errors += errors
    response.data = Data(
        raws,
        dfbuilder=partial(
            historical_build_df_multi_inst,
            universe=universe,
            fields=fields,
            axis_name=axis_name,
        ),
    )
    response._status = http_statuses
    response.http_response = http_responses

    return response
