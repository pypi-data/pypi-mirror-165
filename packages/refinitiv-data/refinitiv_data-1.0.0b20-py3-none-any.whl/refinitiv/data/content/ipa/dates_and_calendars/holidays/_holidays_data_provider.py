from typing import List

import pandas as pd
from dateutil import parser
from pandas.tseries.holiday import nearest_workday, Holiday

from ....._tools import create_repr
from .._content_data_validator import ContentDataValidator
from ...._df_builder import build_dates_calendars_holidays_df
from .....content.ipa._content_provider import DatesAndCalendarsRequestFactory
from .....delivery._data._data_provider import (
    ResponseFactory,
    DataProvider,
    ValidatorContainer,
    Data,
)


class HolidayName:
    def __init__(self, name: str, calendars: list, countries: list):
        self._name = name
        self._calendars = calendars
        self._countries = countries

    @property
    def name(self):
        return self._name

    @property
    def countries(self):
        return self._countries

    @property
    def calendars(self):
        return self._calendars


class HolidayData(Holiday):
    def __init__(self, holiday: dict, tag: str = ""):
        self._holiday = holiday

        if self._holiday.get("names"):
            name = self._holiday.get("names")[0]["name"]
        else:
            name = "Name not requested"

        date = self._holiday.get("date")

        year, month, day = pd.NA, pd.NA, pd.NA
        if date:
            date = parser.parse(date)
            year, month, day = date.year, date.month, date.day

        Holiday.__init__(
            self,
            name=name,
            year=year,
            month=month,
            day=day,
            observance=nearest_workday,
        )

        self._date = holiday.get("date", "Date not requested")
        self._tag = tag
        self._countries = holiday.get("countries", [])
        self._calendars = holiday.get("calendars", [])
        self._holiday_names = []

    @property
    def date(self):
        return self._date

    @property
    def countries(self):
        return self._countries

    @property
    def calendars(self):
        return self._calendars

    @property
    def names(self) -> List[HolidayName]:
        if self._holiday_names:
            return self._holiday_names

        for holiday_name in self._holiday.get("names", []):
            self._holiday_names.append(
                HolidayName(
                    name=holiday_name["name"],
                    calendars=holiday_name["calendars"],
                    countries=holiday_name["countries"],
                )
            )
        return self._holiday_names

    @property
    def tag(self):
        return self._tag

    def __repr__(self):
        return create_repr(
            self,
            class_name="HolidayData",
            content="representation of 'holidayOutputs' response",
        )


class HolidaysData(Data):
    def __init__(self, raw: dict):
        super().__init__(raw, dfbuilder=build_dates_calendars_holidays_df)
        self._holidays = []
        self._holidays_data = []

    @property
    def holidays(self) -> List[HolidayData]:
        if self._holidays:
            return self._holidays

        for raw_item in self.raw:
            if not raw_item.get("error"):
                self._holidays_data.append(raw_item)

        for item in self._holidays_data:
            for holiday in item["holidays"]:
                holiday_ = HolidayData(holiday, item.get("tag"))
                self._holidays.append(holiday_)
        return self._holidays


class HolidaysResponseFactory(ResponseFactory):
    def create_success(self, data: dict, *args: tuple, **kwargs: dict):
        response = self.response_class(is_success=True, **data)
        holidays_data = HolidaysData(data.get("content_data"))
        response.data = holidays_data

        return response

    def create_fail(self, data: dict, *args: tuple, **kwargs: dict):
        if data.get("status", {}).get("error", {}).get("errors"):
            message = data["status"]["error"]["errors"][0]["reason"]
            data["error_message"] = f"{data['error_message']}. {message}"

        return super().create_fail(data, *args, **kwargs)


holidays_data_provider = DataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=HolidaysResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
