import asyncio
import re
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List

from ._intervals import DayIntervalType
from ._join_responses import get_first_success_response
from ._types import Strings
from .._errors import RDError
from ..delivery._data import _data_provider
from ..delivery._data._data_provider import (
    DataProvider,
    Response,
    ResponseFactory,
    ContentValidator,
)

user_has_no_permissions_expr = re.compile(
    r"TS\.((Interday)|(Intraday))\.UserNotPermission\.[0-9]{5}"
)


# ---------------------------------------------------------------------------
#   Raw data parser
# ---------------------------------------------------------------------------


class ErrorParser(_data_provider.Parser):
    def process_failed_response(self, raw_response):
        parsed_data = super().process_failed_response(raw_response)
        status = parsed_data.get("status", {})
        error = status.get("error", {})
        errors = error.get("errors", [])
        error_code = parsed_data.get("error_code")
        error_message = parsed_data.get("error_message", "")
        err_msgs = []
        err_codes = []
        for err in errors:
            reason = err.get("reason")
            if reason:
                err_codes.append(error_code)
                err_msgs.append(f"{error_message}: {reason}")

        if err_msgs and err_codes:
            parsed_data["error_code"] = err_codes
            parsed_data["error_message"] = err_msgs

        return parsed_data


# ---------------------------------------------------------------------------
#   Content data validator
# ---------------------------------------------------------------------------


def get_invalid_universes(universes):
    result = []
    for universe in universes:
        if universe.get("Organization PermID") == "Failed to resolve identifier(s).":
            result.append(universe.get("Instrument"))
    return result


def get_universe_from_raw_response(raw_response):
    universe = raw_response.url.params["universe"]
    universe = universe.split(",")
    return universe


class UniverseContentValidator(_data_provider.ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = super().validate(data)
        if not is_valid:
            return is_valid

        content_data = data.get("content_data", {})
        error = content_data.get("error", {})
        universes = content_data.get("universe", [])
        invalid_universes = get_invalid_universes(universes)

        if error:
            is_valid = False
            data["error_code"] = error.get("code")

            error_message = error.get("description")
            if error_message == "Unable to resolve all requested identifiers.":
                universe = get_universe_from_raw_response(data["raw_response"])
                error_message = f"{error_message} Requested items: {universe}"

            if not error_message:
                error_message = error.get("message")
                errors = error.get("errors")
                if isinstance(errors, list):
                    errors = "\n".join(map(str, errors))
                    error_message = f"{error_message}:\n{errors}"
            data["error_message"] = error_message

        elif invalid_universes:
            data["error_message"] = f"Failed to resolve identifiers {invalid_universes}"

        return is_valid


class HistoricalContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        content_data = data.get("content_data")

        if not content_data:
            is_valid = False

        elif isinstance(content_data, list) and len(content_data):
            content_data = content_data[0]
            status = content_data.get("status", {})
            code = status.get("code", "")

            if status and user_has_no_permissions_expr.match(code):
                is_valid = False
                data["status"]["error"] = status
                data["errors"] = [(code, status.get("message"))]

            elif "Error" in code:
                is_valid = False
                data["status"]["error"] = status
                data["errors"] = [(code, status.get("message"))]

                if not (content_data.keys() - {"universe", "status"}):
                    is_valid = False

                elif "UserRequestError" in code:
                    is_valid = True

            elif not content_data.get("data"):
                is_valid = False

        return is_valid


# ---------------------------------------------------------------------------
#   Provider layer
# ---------------------------------------------------------------------------


class ContentProviderLayer(_data_provider.DataProviderLayer):
    def __init__(self, content_type, **kwargs):
        _data_provider.DataProviderLayer.__init__(
            self,
            data_type=content_type,
            **kwargs,
        )


# --------------------------------------------------------------------------------------
#   Response
# --------------------------------------------------------------------------------------


response_errors = {
    "default": "{error_message}. Requested ric: {rics}. Requested fields: {fields}",
    "TS.Intraday.UserRequestError.90001": "{rics} - The universe is not found",
    "TS.Intraday.Warning.95004": "{rics} - Trades interleaving with corrections is "
    "currently not supported. Corrections will not be returned.",
    "TS.Intraday.UserRequestError.90006": "{error_message} Requested ric: {rics}",
}


class HistoricalResponseFactory(ResponseFactory):
    def get_raw(self, data):
        raw = data.get("content_data", [{}])
        raw = raw[0]
        return raw

    def create_success(self, data, *args, **kwargs):
        raw = self.get_raw(data)
        error_code = data.get("status_code") or (
            raw.get("status").get("code") if raw.get("status") else None
        )
        if error_code:
            self._compile_error_message(error_code, data, **kwargs)
        return super().create_success(data, *args, **kwargs)

    def create_fail(self, data, *args, **kwargs):
        raw = self.get_raw(data)
        status = raw.get("status", {})
        error_code = data.get("error_code", status.get("code"))
        self._compile_error_message(error_code, data, **kwargs)
        return super().create_fail(data, *args, **kwargs)

    @staticmethod
    def _compile_error_message(error_code: str, data: dict, **kwargs):
        """Compile error message in human readable format."""
        content_data = data.get("content_data")[0] if data.get("content_data") else {}
        error_message = data.get("error_message") or content_data.get("status", {}).get(
            "message"
        )
        fields = kwargs.get("fields")
        rics = (
            content_data.get("universe").get("ric")
            if content_data
            else kwargs.get("universe")
        )

        if error_code not in response_errors.keys():
            # Need to add error_code to data because different structure of responses
            data["error_code"] = error_code
            data["error_message"] = response_errors["default"].format(
                error_message=error_message, rics=rics, fields=fields
            )
        else:
            data["error_code"] = error_code
            data["error_message"] = response_errors[error_code].format(
                rics=rics, error_message=error_message
            )


# ---------------------------------------------------------------------------
#   DataProvider
# ---------------------------------------------------------------------------


class HistoricalDataProvider(DataProvider):
    @staticmethod
    @abstractmethod
    def _join_responses(
        responses: List[Response], universe: Strings, fields: Strings, kwargs
    ):
        pass

    async def _create_task(self, name, *args, **kwargs) -> Response:
        kwargs["universe"] = name
        response = await super().get_data_async(*args, **kwargs)
        return response

    def get_data(self, *args, **kwargs) -> Response:
        universe: List[str] = kwargs.pop("universe", [])
        fields = copy_fields(kwargs.get("fields"))

        with ThreadPoolExecutor(
            thread_name_prefix="HistoricalRequestParallel"
        ) as executor:

            futures = []
            for inst_name in universe:
                fut = executor.submit(
                    super().get_data, *args, universe=inst_name, **kwargs
                )
                futures.append(fut)
            wait(futures)

            responses = []
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception
                responses.append(fut.result())

        validate_responses(responses)
        return self._join_responses(responses, universe, fields, kwargs)

    async def get_data_async(self, *args, **kwargs) -> Response:
        universe = kwargs.get("universe", [])
        fields = copy_fields(kwargs.get("fields"))
        tasks = []
        for inst_name in universe:
            tasks.append(self._create_task(inst_name, *args, **kwargs))

        responses = await asyncio.gather(*tasks)
        return self._join_responses(responses, universe, fields, kwargs)


def copy_fields(fields: List[str]) -> List[str]:
    if fields is None:
        return []

    if not isinstance(fields, list):
        raise AttributeError(f"fields not support type {type(fields)}")

    return fields[:]


def validate_responses(responses: List[Response]):
    response = get_first_success_response(responses)
    if response is None:
        error_message = "ERROR: No successful response.\n"
        error_codes = set()
        for response in responses:
            if response.errors:
                error = response.errors[0]
                if error.code not in error_codes:
                    error_codes.add(error.code)
                    sub_error_message = error.message
                    if "." in error.message:
                        sub_error_message, _ = error.message.split(".", maxsplit=1)
                    error_message += f"({error.code}, {sub_error_message}), "
        error_message = error_message[:-2]
        raise RDError(1, f"No data to return, please check errors: {error_message}")


field_timestamp_by_day_interval_type = {
    DayIntervalType.INTER: "DATE",
    DayIntervalType.INTRA: "DATE_TIME",
}
axis_by_day_interval_type = {
    DayIntervalType.INTRA: "Timestamp",
    DayIntervalType.INTER: "Date",
}
