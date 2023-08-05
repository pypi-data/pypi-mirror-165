from datetime import datetime
from .._content_data_validator import ContentDataValidator
from ...._df_builder import build_dates_calendars_date_schedule_df
from .....content.ipa._content_provider import (
    DatesAndCalendarsDateScheduleRequestFactory,
)
from .....delivery._data._data_provider import (
    ResponseFactory,
    DataProvider,
    ValidatorContainer,
    Data,
)


class DateSchedule(Data):
    def __init__(self, raw: dict):
        super().__init__(raw, dfbuilder=build_dates_calendars_date_schedule_df)
        self._dates = []

    @property
    def dates(self):
        if self._dates:
            return self._dates

        dates = []
        for date in self.raw["dates"]:
            date = datetime.strptime(date, "%Y-%m-%d")
            dates.append(date)
        return dates


class DateScheduleResponseFactory(ResponseFactory):
    def create_success(self, data: dict, *args: tuple, **kwargs: dict):
        response = self.response_class(is_success=True, **data)
        date_schedule = DateSchedule(data.get("content_data"))
        response.data = date_schedule
        return response

    def create_fail(self, data: dict, *args: tuple, **kwargs: dict):
        if data.get("status", {}).get("error", {}).get("errors"):
            message = data["status"]["error"]["errors"][0]["reason"]
            data["error_message"] = f"{data['error_message']}. {message}"

        return super().create_fail(data, *args, **kwargs)


date_schedule_data_provider = DataProvider(
    request=DatesAndCalendarsDateScheduleRequestFactory(),
    response=DateScheduleResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
