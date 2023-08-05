from itertools import zip_longest
from typing import Any

import numpy
import pandas as pd
from pandas import DataFrame

from ..._content_provider import ErrorParser
from ...._tools import (
    ArgsParser,
    fields_arg_parser,
)
from ...._tools._dataframe import convert_column_df_to_datetime
from ....delivery._data._data_provider import ContentValidator, ValidatorContainer
from ....delivery._data._data_provider import (
    RequestFactory,
    DataProvider,
    ResponseFactory,
    Data as ContentData,
)
from ....delivery.endpoint_request import RequestMethod


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class ContractsContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        content_data = data.get("content_data")
        status = content_data.get("status", "")

        if content_data is None:
            data["error_code"] = 1
            data["error_message"] = "Content data is None"
            return False

        elif status == "Error":
            data["error_code"] = content_data.get("code")
            data["error_message"] = content_data.get("message")
            return False

        else:
            return self._is_valid_if_have_all_errors(data, content_data)

    def _is_valid_if_have_all_errors(self, data: dict, content_data: dict) -> bool:
        headers = content_data.get("headers", [])
        datas = content_data.get("data", [])
        err_codes = []
        err_msgs = []

        for header, *data_items in zip(headers, *datas):
            header_name = header["name"]

            if "ErrorCode" == header_name:
                err_codes = data_items

            elif "ErrorMessage" == header_name:
                err_msgs = data_items

        counter = len(datas) or 1  # because datas can be empty list
        if err_codes or err_msgs:
            for err_code, err_msg in zip_longest(err_codes, err_msgs, fillvalue=None):
                if err_code or err_msg:
                    counter -= 1
                    error_codes = data.setdefault("error_code", [])
                    error_codes.append(err_code)
                    error_messages = data.setdefault("error_message", [])
                    error_messages.append(err_msg)

        if counter == 0:
            return False

        return True


# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------


def convert_data_items_to_datetime(df: pd.DataFrame, headers) -> pd.DataFrame:
    for index, header in enumerate(headers):
        header_type = header.get("type", "")
        if header_type == "DateTime" or header_type == "Date":
            convert_column_df_to_datetime(df, index)

    return df


def financial_contracts_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    """
    Convert "data" from raw response bond to dataframe format
    """
    data = raw.get("data")
    headers = raw.get("headers")
    if data:
        numpy_array = numpy.array(data, dtype=object)
        df = DataFrame(numpy_array)
        df = convert_data_items_to_datetime(df, headers)
        df.columns = [header["name"] for header in headers]
        if not df.empty:
            df.fillna(pd.NA, inplace=True)
            df = df.convert_dtypes()
    else:
        df = DataFrame([], columns=[])
    return df


class Data(ContentData):
    """
    This class is designed for storing and managing the response instrument data
    """

    def __init__(self, raw, **kwargs):
        super().__init__(raw, **kwargs)
        self._analytics_headers = None
        self._analytics_data = None
        self._analytics_market_data = None
        self._analytics_statuses = None
        if raw:
            #   get headers
            self._analytics_headers = raw.get("headers")
            #   get data
            self._analytics_data = raw.get("data")
            #   get marketData
            self._analytics_market_data = raw.get("marketData")
            #   get statuses
            self._analytics_statuses = raw.get("statuses")

    @property
    def analytics_headers(self):
        return self._analytics_headers

    @property
    def analytics_data(self):
        return self._analytics_data

    @property
    def analytics_market_data(self):
        return self._analytics_market_data

    @property
    def analytics_statuses(self):
        return self._analytics_statuses

    @property
    def marketdata_df(self):
        """
        Convert "marketData" from raw response bond to dataframe format
        """
        return None


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class ContractsRequestFactory(RequestFactory):
    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if not extended_params:
            return body_parameters

        if kwargs.get("__plural__") is True:
            body_parameters.update(extended_params)
            return body_parameters

        universes = body_parameters.get("universe", [])
        for item in universes:
            item.get("instrumentDefinition", {}).update(extended_params)
        return body_parameters

    def get_request_method(self, *_, **kwargs):
        return kwargs.get("method", RequestMethod.POST)

    def get_body_parameters(
        self,
        *args,
        universe=None,
        definition=None,
        fields=None,
        outputs=None,
        pricing_parameters=None,
        **kwargs,
    ):
        plural = kwargs.get("__plural__")
        if plural is True:
            input_universe = universe
        else:
            input_universe = [definition]

        universe = []
        for item in input_universe:
            item_defn = item
            item_pricing_parameters = not plural and pricing_parameters
            item_extended_params = None

            if hasattr(item, "_kwargs"):
                kwargs = getattr(item, "_kwargs")
                item_defn = kwargs.get("definition")
                item_pricing_parameters = kwargs.get("pricing_parameters")
                item_extended_params = kwargs.get("extended_params")

            inst_defn_dict = item_defn.get_dict()

            if item_extended_params:
                inst_defn_dict.update(item_extended_params)

            data = {
                "instrumentType": item_defn.get_instrument_type(),
                "instrumentDefinition": inst_defn_dict,
            }

            if item_pricing_parameters:
                data["pricingParameters"] = item_pricing_parameters.get_dict()

            universe.append(data)

        body_parameters = {"universe": universe}

        if fields:
            fields = fields_arg_parser.get_list(fields)
            body_parameters["fields"] = fields

        if pricing_parameters and plural is True:
            body_parameters["pricingParameters"] = pricing_parameters.get_dict()

        return body_parameters


def get_data(definition, pricing_parameters=None):
    fields = None
    extended_params = None

    if hasattr(definition, "_kwargs"):
        kwargs = getattr(definition, "_kwargs")
        definition = kwargs.get("definition")
        fields = kwargs.get("fields")
        pricing_parameters = kwargs.get("pricing_parameters")
        extended_params = kwargs.get("extended_params")

    definition_dict = definition.get_dict()

    if extended_params:
        definition_dict.update(extended_params)

    data = {
        "instrumentType": definition.get_instrument_type(),
        "instrumentDefinition": definition_dict,
    }

    if fields:
        fields = fields_arg_parser.get_list(fields)
        data["fields"] = fields

    if pricing_parameters:
        data["pricingParameters"] = pricing_parameters.get_dict()

    return data


def process_bond_instrument_code(code: Any) -> str:
    if code is None or isinstance(code, str):
        return code
    else:
        raise ValueError(
            f"Invalid type of instrument_code, string is expected."
            f"type: {type(code)} is given"
        )


bond_instrument_code_arg_parser = ArgsParser(process_bond_instrument_code)

# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

contracts_data_provider = DataProvider(
    request=ContractsRequestFactory(),
    response=ResponseFactory(data_class=Data),
    validator=ValidatorContainer(content_validator=ContractsContentValidator()),
    parser=ErrorParser(),
)
