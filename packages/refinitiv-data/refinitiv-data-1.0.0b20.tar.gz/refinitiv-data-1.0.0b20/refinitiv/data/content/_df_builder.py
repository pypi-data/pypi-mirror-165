import abc
from itertools import product
from typing import List, Optional, Any, Set, Tuple, Dict
from copy import deepcopy

import pandas as pd
from pandas.core.tools.datetimes import DatetimeScalarOrArrayConvertible

from refinitiv.data._tools._dataframe import (
    convert_str_to_datetime,
)
from refinitiv.data.content._types import Strings


class DFBuilder(abc.ABC):
    auto_headers: Optional[List] = None

    @abc.abstractmethod
    def get_headers(self, content_data: dict) -> List[dict]:
        pass

    def get_date_idxs(self, columns: List[str]) -> Set[int]:
        return {idx for idx, col in enumerate(columns) if "date" in col.lower()}

    def build_index(
        self, content_data: dict, use_field_names_in_headers: bool = False, **kwargs
    ) -> pd.DataFrame:

        key = "name" if use_field_names_in_headers else "title"

        headers = self.get_headers(content_data)
        columns = [header[key] for header in headers]
        date_idxs = self.get_date_idxs(columns)

        data = []
        fields_list = content_data.get("data", [])
        for fields in fields_list:
            fields = list(fields)

            for idx, item in enumerate(fields):
                if item is None:
                    fields[idx] = pd.NA

            for idx in date_idxs:
                fields[idx] = convert_str_to_datetime(fields[idx])

            data.append(fields)

        df = pd.DataFrame(data=data, columns=columns)
        return df

    def build_date_as_index(
        self,
        content_data: dict,
        use_field_names_in_headers: bool = False,
        use_multiindex: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        key = "name" if use_field_names_in_headers else "title"

        headers = self.get_headers(content_data)
        columns = [header[key] for header in headers]

        inst_header, date_header = self.auto_headers
        inst_header = inst_header[key]
        date_header = date_header[key]

        data = []
        index = []
        inst_idx = columns.index(inst_header)
        date_idx = columns.index(date_header)
        columns.pop(date_idx)
        columns.pop(inst_idx)
        num_columns = len(columns)

        date_idxs = self.get_date_idxs(columns)
        fields_by_inst_by_date = {}
        fields_list = content_data.get("data", [])
        unique_insts = list(dict.fromkeys(fields[inst_idx] for fields in fields_list))
        num_unique_insts = len(unique_insts)
        for fields in fields_list:
            fields = list(fields)
            date_str = fields[date_idx]

            if not date_str:
                continue

            inst = fields[inst_idx]
            fields.pop(date_idx)
            fields.pop(inst_idx)
            is_add = True

            for idx, item in enumerate(fields):
                if item is None:
                    fields[idx] = pd.NA

            for idx in date_idxs:
                fields[idx] = convert_str_to_datetime(fields[idx])

            if num_unique_insts > 1:
                total = num_unique_insts * num_columns
                template = [pd.NA] * total

                idx = unique_insts.index(inst)
                right_idx = idx * num_columns + num_columns
                left_idx = idx * num_columns
                for item, idx in zip(fields, range(left_idx, right_idx)):
                    template[idx] = item
                fields = template

                fields_by_inst = fields_by_inst_by_date.get(date_str)
                if fields_by_inst and inst not in fields_by_inst.keys():
                    is_add = False
                    idx = max(
                        unique_insts.index(inst) for inst in fields_by_inst.keys()
                    )
                    cache_inst = unique_insts[idx]
                    cache_fields = fields_by_inst[cache_inst]
                    idx = unique_insts.index(inst)
                    cache_idx = unique_insts.index(cache_inst)

                    left_idx = cache_idx * num_columns + num_columns
                    right_idx = idx * num_columns + num_columns

                    for idx in range(left_idx, right_idx):
                        cache_fields[idx] = fields[idx]

                    fields_by_inst[inst] = cache_fields
                    fields = cache_fields

                else:
                    not fields_by_inst and fields_by_inst_by_date.setdefault(
                        date_str, {inst: fields}
                    )
                    date = convert_str_to_datetime(date_str)
                    index.append(date)

            else:
                date = convert_str_to_datetime(date_str)
                index.append(date)

            is_add and data.append(fields)

        if num_unique_insts > 1 or use_multiindex:
            columns = pd.MultiIndex.from_tuples(product(unique_insts, columns))

        elif num_unique_insts == 1:
            columns = pd.Index(data=columns, name=unique_insts.pop())

        index = pd.Index(data=index, name=date_header)
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df.sort_index(ascending=False, inplace=True)
        return df


class DFBuilderRDP(DFBuilder):
    """
    {
        "links": {"count": 2},
        "variability": "",
        "universe": [
            {
                "Instrument": "GOOG.O",
                "Company Common Name": "Alphabet Inc",
                "Organization PermID": "5030853586",
                "Reporting Currency": "USD",
            }
        ],
        "data": [
            ["GOOG.O", "2022-01-26T00:00:00", "USD", None],
            ["GOOG.O", "2020-12-31T00:00:00", None, "2020-12-31T00:00:00"],
        ],
        "messages": {
            "codes": [[-1, -1, -1, -2], [-1, -1, -2, -1]],
            "descriptions": [
                {"code": -2, "description": "empty"},
                {"code": -1, "description": "ok"},
            ],
        },
        "headers": [
            {
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user.",
            },
            {
                "name": "date",
                "title": "Date",
                "type": "datetime",
                "description": "Date associated with the returned data.",
            },
            {
                "name": "TR.RevenueMean",
                "title": "Currency",
                "type": "string",
                "description": "The statistical average of all broker ...",
            },
            {
                "name": "TR.Revenue",
                "title": "Date",
                "type": "datetime",
                "description": "Is used for industrial and utility companies. ...",
            },
        ],
    }
    """

    auto_headers = [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
    ]

    def get_headers(self, content_data) -> List[dict]:
        return content_data.get("headers", [])


class DFBuilderUDF(DFBuilder):
    """
    {
        "columnHeadersCount": 1,
        "data": [
            ["GOOG.O", "2022-01-26T00:00:00Z", "USD", ""],
            ["GOOG.O", "2020-12-31T00:00:00Z", "", "2020-12-31T00:00:00Z"],
        ],
        "headerOrientation": "horizontal",
        "headers": [
            [
                {"displayName": "Instrument"},
                {"displayName": "Date"},
                {"displayName": "Currency", "field": "TR.REVENUEMEAN.currency"},
                {"displayName": "Date", "field": "TR.REVENUE.DATE"},
            ]
        ],
        "rowHeadersCount": 2,
        "totalColumnsCount": 4,
        "totalRowsCount": 3,
    }
    """

    auto_headers = [
        {"name": "Instrument", "title": "Instrument"},
        {"name": "Date", "title": "Date"},
    ]

    def get_headers(self, content_data) -> List[dict]:
        headers = content_data["headers"]
        headers = headers[0]
        return [
            {
                "name": header.get("field") or header.get("displayName"),
                "title": header.get("displayName"),
            }
            for header in headers
        ]


def build_dates_calendars_df(raw: Any, **kwargs):
    raw = deepcopy(raw)
    add_periods_data = []

    clean_request_items = []
    for item in raw:
        if not item.get("error"):
            clean_request_items.append(item)

    for request_item in clean_request_items:
        if request_item.get("date"):
            request_item["date"] = convert_str_to_datetime(request_item["date"])

        request_item.pop("holidays", None)
        add_periods_data.append(request_item)

    _df = pd.DataFrame(add_periods_data)

    return _df


def build_dates_calendars_holidays_df(raw: Any, **kwargs):
    holidays_data = _dates_calendars_prepare_holidays_data(raw)
    holidays_df = pd.DataFrame(holidays_data)
    return holidays_df


def _dates_calendars_prepare_holidays_data(raw):
    raw = deepcopy(raw)
    holidays_data = []

    for request_item_holiday in raw:
        if request_item_holiday.get("holidays"):
            for holiday in request_item_holiday["holidays"]:
                if holiday.get("names"):
                    for holiday_name in holiday["names"]:
                        holiday_name["tag"] = request_item_holiday.get("tag")
                        holiday_name["date"] = convert_str_to_datetime(
                            holiday.get("date")
                        )
                        holidays_data.append(holiday_name)
                else:
                    holiday["tag"] = request_item_holiday.get("tag")
                    holidays_data.append(holiday)
    return holidays_data


def default_build_df(raw: Any, **kwargs) -> pd.DataFrame:
    df = pd.DataFrame(raw)
    return df


def build_dates_calendars_date_schedule_df(raw: Any, **kwargs) -> pd.DataFrame:
    raw = deepcopy(raw)

    _dates = []
    for date in raw.get("dates"):
        _dates.append(convert_str_to_datetime(date))

    raw["dates"] = _dates
    df = pd.DataFrame(raw)
    return df


def build_empty_df(*args, **kwargs) -> pd.DataFrame:
    return pd.DataFrame()


def historical_build_df_one_inst(
    raw: dict, fields: Strings, axis_name: str
) -> pd.DataFrame:
    inst_name = raw["universe"]["ric"]
    data, columns, index = process_historical_raw(raw, fields)
    columns = pd.Index(data=columns, name=inst_name)
    index = pd.Index(data=index, name=axis_name)
    df = pd.DataFrame(data=data, columns=columns, index=index)
    df.sort_index(inplace=True)
    return df


def process_historical_raw(
    raw: dict, fields: Strings
) -> Tuple[List[list], Strings, List[DatetimeScalarOrArrayConvertible]]:
    listoflists = raw["data"]
    headers = raw["headers"]
    headers_names = [header["name"] for header in headers]

    timestamp_name = None
    if "DATE_TIME" in headers_names:
        timestamp_name = "DATE_TIME"
    elif "DATE" in headers_names:
        timestamp_name = "DATE"

    timestamp_index = headers_names.index(timestamp_name)

    if fields:
        data = []
        index = []
        for l in listoflists:
            index.append(convert_str_to_datetime(l[timestamp_index]))
            newl = []
            for field in fields:
                if field in headers_names:
                    item = l[headers_names.index(field)]
                    newl.append(pd.NA if item is None else item)
                else:
                    newl.append(pd.NA)
            data.append(newl)
        columns = fields

    else:
        data = []
        index = []
        for l in listoflists:
            newl = []
            for item, hdr_name in zip(l, headers_names):
                if timestamp_name == hdr_name:
                    index.append(convert_str_to_datetime(item))
                    continue
                newl.append(pd.NA if item is None else item)
            data.append(newl)
        headers_names.pop(timestamp_index)
        columns = headers_names

    return data, columns, index


def historical_build_df_multi_inst(
    raws: List[dict], universe: Strings, fields: Strings, axis_name: str
) -> pd.DataFrame:
    items_by_date: Dict[str, list] = {}
    listofcolumns = []
    listofcolumns_append = listofcolumns.append
    listofcolumns_insert = listofcolumns.insert
    num_raws = len(raws)
    bad_raws = []
    bad_raws_append = bad_raws.append
    num_fields = len(fields)
    raw_columns = None
    for instidx, raw in enumerate(raws):
        # it means error in response for custom instruments
        if not raw:
            raw = {"universe": {"ric": universe[instidx]}}
            bad_raws_append((instidx, raw))
            continue

        # it means error in response for historical pricing
        if isinstance(raw, list):
            raw = raw[0]
            bad_raws_append((instidx, raw))
            continue

        else:
            raw_datas, raw_columns, raw_index = process_historical_raw(raw, fields)

        for date, raw_data in zip(raw_index, raw_datas):
            items = items_by_date.setdefault(date, [])
            items.append((instidx, raw_data, raw_columns))

        inst_name = raw["universe"]["ric"]
        if num_fields == 1:
            processed_columns = [inst_name]

        else:
            processed_columns = list(product([inst_name], raw_columns))

        listofcolumns_append(processed_columns)

    last_raw_columns = raw_columns

    if bad_raws:
        for idx, bad_raw in bad_raws:
            raw_columns = fields or last_raw_columns or "Field"
            inst_name = bad_raw["universe"]["ric"]
            if num_fields == 1:
                processed_columns = [inst_name]

            else:
                processed_columns = list(product([inst_name], raw_columns))

            listofcolumns_insert(idx, processed_columns)

    left_num_columns = {
        split_idx: sum([len(subcols) for subcols in listofcolumns[:split_idx]])
        for split_idx in range(num_raws)
    }

    allcolumns = [col for subcolumns in listofcolumns for col in subcolumns]

    num_allcolumns = len(allcolumns)
    data = []
    index = []
    data_append = data.append
    index_append = index.append
    for date, items in items_by_date.items():
        prev_idx = None
        counter = 0
        num_items = len(items)

        if num_items > 1:
            template = [pd.NA] * num_allcolumns
            for instidx, raw_data, raw_columns in items:
                if (counter != 0 and counter % num_raws == 0) or prev_idx == instidx:
                    index_append(date)
                    data_append(template)
                    template = [pd.NA] * num_allcolumns
                    prev_idx = instidx

                if prev_idx is None:
                    prev_idx = instidx

                counter += 1

                left_idx = left_num_columns[instidx]
                right_idx = left_idx + len(raw_columns)
                for item, i in zip(raw_data, range(left_idx, right_idx)):
                    template[i] = item

            index_append(date)
            data_append(template)

        else:
            index_append(date)
            instidx, raw_data, raw_columns = items[0]
            left = [pd.NA] * left_num_columns[instidx]
            right = [pd.NA] * (num_allcolumns - len(raw_columns) - len(left))
            data_append(left + raw_data + right)

    if num_fields == 1:
        columns = pd.Index(data=allcolumns, name=fields[0])

    else:
        columns = pd.MultiIndex.from_tuples(allcolumns)

    index = pd.Index(data=index, name=axis_name)
    df = pd.DataFrame(data=data, columns=columns, index=index)
    df.sort_index(inplace=True)
    return df


dfbuilder_rdp = DFBuilderRDP()
dfbuilder_udf = DFBuilderUDF()
