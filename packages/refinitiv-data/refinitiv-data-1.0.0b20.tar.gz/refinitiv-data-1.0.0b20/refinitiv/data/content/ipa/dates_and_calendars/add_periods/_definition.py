from datetime import datetime, timedelta
from typing import List, Optional, Union

from numpy import iterable

from ._add_periods_data_provider import AddedPeriod, AddedPeriods
from .._base_request_items import StartDateBase
from ..._enums import DateMovingConvention, EndOfMonthConvention, HolidayOutputs
from ....._tools import create_repr

from ...._content_type import ContentType
from .....delivery._data._data_provider import DataProviderLayer, BaseResponse
from ...._types import ExtendedParams


class DatePeriodsRequestItem(StartDateBase):
    def __init__(
        self,
        start_date: Union[str, datetime, timedelta],
        period: str,
        calendars: Optional[List[str]] = None,
        currencies: Optional[List[str]] = None,
        tag: Optional[str] = None,
        date_moving_convention: Optional[DateMovingConvention] = None,
        end_of_month_convention: Optional[EndOfMonthConvention] = None,
        holiday_outputs: Optional[List[HolidayOutputs]] = None,
    ):
        super().__init__(start_date)
        self.tag = tag
        self.period = period
        self.calendars = calendars
        self.currencies = currencies
        self.date_moving_convention = date_moving_convention
        self.end_of_month_convention = end_of_month_convention
        self.holiday_outputs = holiday_outputs

    @property
    def tag(self):
        """
        :return: str
        """
        return self._get_parameter("tag")

    @tag.setter
    def tag(self, value):
        self._set_parameter("tag", value)

    @property
    def period(self):
        """
        :return: str
        """
        return self._get_parameter("period")

    @period.setter
    def period(self, value):
        self._set_parameter("period", value)

    @property
    def calendars(self):
        """
        :return: list
        """
        return self._get_parameter("calendars")

    @calendars.setter
    def calendars(self, value):
        self._set_parameter("calendars", value)

    @property
    def currencies(self):
        """
        :return: list
        """
        return self._get_parameter("currencies")

    @currencies.setter
    def currencies(self, value):
        self._set_parameter("currencies", value)

    @property
    def date_moving_convention(self):
        """
        :return: DateMovingConvention
        """
        return self._get_enum_parameter(DateMovingConvention, "dateMovingConvention")

    @date_moving_convention.setter
    def date_moving_convention(self, value):
        self._set_enum_parameter(DateMovingConvention, "dateMovingConvention", value)

    @property
    def end_of_month_convention(self):
        """
        :return: EndOfMonthConvention
        """
        return self._get_enum_parameter(EndOfMonthConvention, "endOfMonthConvention")

    @end_of_month_convention.setter
    def end_of_month_convention(self, value):
        self._set_enum_parameter(EndOfMonthConvention, "endOfMonthConvention", value)

    @property
    def holiday_outputs(self):
        """
        :return: list
        """
        return self._get_list_of_enums(HolidayOutputs, "holidayOutputs")

    @holiday_outputs.setter
    def holiday_outputs(self, value):
        self._set_list_of_enums(HolidayOutputs, "holidayOutputs", value)


class Definition(DataProviderLayer[BaseResponse[AddedPeriod]]):
    """
    Add periods definition object

    Parameters
    ----------
        start_date: str or datetime or timedelta
            Start date of calculation.
        period: str
            String representing the tenor.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        tag: str, optional
            Reference tag to map particular response in payload.
        date_moving_convention : DateMovingConvention or str, optional
            The method to adjust dates.
        end_of_month_convention : EndOfMonthConvention or str, optional
            End of month convention.
        holiday_outputs : HolidayOutputs or list of str, optional
            In case if test date is holiday you may request additional information about the holiday.
            Possible options are: Date, Names, Calendars, Countries
        extended_params : dict, optional
            If necessary other parameters.

    Methods
    -------
    get_data(session=None, on_response=None, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
     >>> from refinitiv.data.content.ipa.dates_and_calendars import add_periods
     >>> definition = add_periods.Definition(
     ...     tag="my request",
     ...     start_date="2020-01-01",
     ...     period="4D",
     ...         calendars=["BAR", "KOR", "JAP"],
     ...         currencies=["USD"],
     ...     ),
     ...     calendars=["BAR", "KOR", "JAP"],
     ...     currencies=["USD"],
     ...     date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
     ...     end_of_month_convention=add_periods.EndOfMonthConvention.LAST,
     ...     holiday_outputs=["Date", "Calendars", "Names"]
     ... )
     >>> response = definition.get_data()

     Using get_data_async
     >>> import asyncio
     >>> task = definition.get_data_async()
     >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        start_date: Union[str, datetime, timedelta],
        period: str,
        calendars: Optional[List[str]] = None,
        currencies: Optional[List[str]] = None,
        tag: Optional[str] = None,
        date_moving_convention: Optional[Union[DateMovingConvention, str]] = None,
        end_of_month_convention: Optional[Union[EndOfMonthConvention, str]] = None,
        holiday_outputs: Optional[Union[List[HolidayOutputs], List[str]]] = None,
        extended_params: ExtendedParams = None,
    ):
        self.extended_params = extended_params

        self.request_item = DatePeriodsRequestItem(
            start_date=start_date,
            period=period,
            calendars=calendars,
            currencies=currencies,
            tag=tag,
            date_moving_convention=date_moving_convention,
            end_of_month_convention=end_of_month_convention,
            holiday_outputs=holiday_outputs,
        )

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_ADD_PERIODS,
            universe=[self.request_item],
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


class Definitions(DataProviderLayer[BaseResponse[Union[AddedPeriods]]]):
    """
    Add periods definitions object

    Parameters
    ----------
    universe: Definition or list of Definition objects
        List of initialized Definition objects to retrieve data.

    Methods
    -------
    get_data(session=None, on_response=None, **kwargs)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, **kwargs)
        Returns a response asynchronously to the data platform

    Examples
    --------
     >>> import datetime
     >>> from refinitiv.data.content.ipa.dates_and_calendars import add_periods
     >>>
     >>> first_definition = add_periods.Definition(
     ...     tag="first",
     ...     start_date="2020-01-01",
     ...     period="4D",
     ...     calendars=["BAR", "KOR", "JAP"],
     ...     currencies=["USD"],
     ...     date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
     ...     end_of_month_convention=add_periods.EndOfMonthConvention.LAST,
     ...     holiday_outputs=["Date", "Calendars", "Names"]
     ... )
     >>> second_definition = add_periods.Definition(
     ...     tag="second",
     ...     start_date="2018-01-01",
     ...     period="4D",
     ...     calendars=["BAR", "JAP"],
     ...     currencies=["USD"],
     ...     date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
     ...     end_of_month_convention=add_periods.EndOfMonthConvention.LAST28,
     ...     holiday_outputs=[add_periods.HolidayOutputs.DATE, add_periods.HolidayOutputs.NAMES]
     ... )
     >>> response = add_periods.Definitions([first_definition, second_definition]).get_data()

    Using get_data_async
     >>> import asyncio
     >>> task = add_periods.Definitions([first_definition, second_definition]).get_data_async()
     >>> response = asyncio.run(task)
    """

    def __init__(self, universe: Union[List[Definition], Definition]):
        if not iterable(universe):
            universe = [universe]

        request_items = []
        extended_params = []
        for item in universe:
            request_items.append(item.request_item)
            extended_params.append(item.extended_params)

        super().__init__(
            data_type=ContentType.DATES_AND_CALENDARS_ADD_PERIODS,
            universe=request_items,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)
