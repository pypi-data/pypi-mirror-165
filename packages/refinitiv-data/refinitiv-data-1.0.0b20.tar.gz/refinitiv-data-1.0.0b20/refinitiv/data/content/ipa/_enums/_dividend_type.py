# coding: utf8

from enum import Enum, unique


@unique
class DividendType(Enum):
    FORECAST_TABLE = "ForecastTable"
    FORECAST_YIELD = "ForecastYield"
    FUTURES = "Futures"
    HISTORICAL_YIELD = "HistoricalYield"
    IMPLIED_TABLE = "ImpliedTable"
    IMPLIED_YIELD = "ImpliedYield"
    NONE = "None"
