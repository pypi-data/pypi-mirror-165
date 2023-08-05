from ..holidays._holidays_data_provider import HolidayData
from .._content_data_validator import ContentDataValidator
from ...._df_builder import build_dates_calendars_df
from .....content.ipa._content_provider import DatesAndCalendarsRequestFactory
from .....delivery._data._data_provider import (
    ResponseFactory,
    DataProvider,
    ValidatorContainer,
    Data,
)


class Period:
    def __init__(self, date: str, holidays: list = None, tag: str = ""):
        self._date = date
        self._response_holidays_items = holidays or []
        self._tag = tag
        self._holidays = []

    @property
    def tag(self):
        return self._tag

    @property
    def date(self):
        return self._date

    @property
    def holidays(self):
        if self._holidays:
            return self._holidays

        for holiday in self._response_holidays_items:
            holiday_ = HolidayData(holiday, self.tag)
            self._holidays.append(holiday_)
        return self._holidays


class AddedPeriods(Data):
    def __init__(self, raw: dict):
        super().__init__(raw, dfbuilder=build_dates_calendars_df)
        self._raw = raw
        self._added_periods = []

        self._periods_data = []
        for raw_item in self._raw:
            if not raw_item.get("error"):
                self._periods_data.append(raw_item)

        for item in self._periods_data:
            added_period = Period(
                date=item["date"], holidays=item.get("holidays"), tag=item.get("tag")
            )
            self._added_periods.append(added_period)

    @property
    def added_periods(self):
        return self._added_periods

    def __getitem__(self, item):
        return self._added_periods[item]


class AddedPeriod(Data):
    def __init__(self, raw: dict, date: str, holidays: None, tag: str = ""):
        super().__init__(raw, dfbuilder=build_dates_calendars_df)
        self._period = Period(date=date, holidays=holidays, tag=tag)

    @property
    def added_period(self):
        return self._period


class AddPeriodsResponseFactory(ResponseFactory):
    def create_success(self, data: dict, *args: tuple, **kwargs: dict):
        response = self.response_class(is_success=True, **data)

        if len(response.data) > 1:
            added_periods = AddedPeriods(raw=data.get("content_data"))
            response.data = added_periods
        else:
            raw_response_item = response.data[0]
            response.data = AddedPeriod(
                raw=data.get("content_data"),
                date=raw_response_item["date"],
                holidays=raw_response_item.get("holidays"),
                tag=raw_response_item.get("tag"),
            )

        return response

    def create_fail(self, data: dict, *args: tuple, **kwargs: dict):
        if data.get("status", {}).get("error", {}).get("errors"):
            message = data["status"]["error"]["errors"][0]["reason"]
            data["error_message"] = f"{data['error_message']}. {message}"

        return super().create_fail(data, *args, **kwargs)


add_period_data_provider = DataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=AddPeriodsResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
