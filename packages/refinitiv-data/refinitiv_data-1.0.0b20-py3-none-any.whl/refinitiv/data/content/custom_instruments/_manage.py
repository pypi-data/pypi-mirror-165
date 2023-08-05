from typing import Optional, List, Union

from ._custom_instrument_types import CustomInstrumentTypes
from .._content_type import ContentType
from .._types import ExtendedParams

from ...delivery._data._data_provider import DataProviderLayer, Response
from ...delivery._data._endpoint_data import RequestMethod


class CustomInstrument:
    def __init__(
        self,
        symbol,
        formula,
        instrument_name=None,
        exchange_name=None,
        currency=None,
        time_zone=None,
        holidays=None,
        description=None,
        udc=None,
        basket=None,
        type_=None,
        session=None,
    ):
        """
        symbol : str
            Instrument symbol in the format "S)someSymbol.YOURUUID".
        formula : str
            Formula consisting of rics (fields can be specified by comma).
        instrument_name : str, optional
            Human-readable name of the instrument. Maximum of 16 characters.
        exchange_name : str, optional
            4-letter code of the listing exchange.
        currency : str, optional
            3-letter code of the currency of the instrument, e.g. GBP.
        time_zone: str, optional
            Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
        holidays : list[dict], optional
            List of custom calendar definitions.
        description : str, optional
            Free text field from the user to put any notes or text. Up to 1000 characters.
        basket : dict, optional
            For weighted baskets / indices.
        udc : dict, optional
            Custom trading sessions, see sample format below.

        """
        self.symbol = symbol
        self.formula = formula
        self.instrument_name = instrument_name
        self.exchange_name = exchange_name
        self.currency = currency
        self.time_zone = time_zone
        self.holidays = holidays
        self.description = description
        self.udc = udc
        self.basket = basket
        self.type = type_
        self.id = None
        self.owner = None
        self._session = session

    def delete(self):
        data_provider_layer = DataProviderLayer(
            data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS, universe=self.symbol
        )
        data_provider_layer.get_data(self._session, method=RequestMethod.DELETE)

    def _update(self, data):
        self.symbol = data.get("symbol")
        self.formula = data.get("formula")
        self.instrument_name = data.get("instrumentName")
        self.exchange_name = data.get("exchangeName")
        self.currency = data.get("currency")
        self.time_zone = data.get("timeZone")
        self.holidays = data.get("holidays")
        self.description = data.get("description")
        self.id = data.get("id")
        self.type = data.get("type")
        self.owner = data.get("owner")
        self.udc = data.get("udc")
        self.basket = data.get("basket")

    def save(self):
        data = {
            "symbol": self.symbol,
            "formula": self.formula,
            "instrument_name": self.instrument_name,
            "exchange_name": self.exchange_name,
            "currency": self.currency,
            "time_zone": self.time_zone,
            "holidays": self.holidays,
            "description": self.description,
            "id": self.id,
            "type_": self.type,
            "owner": self.owner,
            "udc": self.udc,
            "basket": self.basket,
        }
        data_provider_layer = DataProviderLayer(
            data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
            universe=self.id,
            **data,
        )
        response = data_provider_layer.get_data(self._session, method=RequestMethod.PUT)

        self._update(response.data.raw)


def delete(
    universe,
    extended_params: "ExtendedParams" = None,
    session=None,
) -> Response:
    """
    universe : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import delete
    >>> response = delete("MyInstrument")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
        extended_params=extended_params,
    )
    return data_provider_layer.get_data(session, method=RequestMethod.DELETE)


def get(
    universe, extended_params: "ExtendedParams" = None, session=None
) -> CustomInstrument:
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS, universe=universe
    )
    response = data_provider_layer.get_data(
        method=RequestMethod.GET, extended_params=extended_params, session=session
    )
    data = response.data.raw
    symbol = data.get("symbol")
    formula = data.get("formula")
    ci = CustomInstrument(symbol=symbol, formula=formula)
    ci._update(data)
    return ci


def create(
    symbol: str,
    formula: Optional[str] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    currency: Optional[str] = None,
    time_zone: Optional[str] = None,
    holidays: Optional[List[dict]] = None,
    description: Optional[str] = None,
    type_: Union[str, CustomInstrumentTypes] = CustomInstrumentTypes.Formula,
    basket: Optional[dict] = None,
    udc: Optional[dict] = None,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
) -> CustomInstrument:
    """
    symbol : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    formula : str
        Formula consisting of rics (fields can be specified by comma).
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    time_zone: str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    holidays : list[dict], optional
        List of custom calendar definitions.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    type_ : str or CustomInstrumentType, optional
        Determines the kind of custom instrument
        "formula", referring to a synthetic RIC formed by a formula combining RICs.
        "udc" for user-defined continuations.
        "basket" for weighted baskets / indices.
        If not specified or blank, the default is "formula".
    basket : dict, optional
        For weighted baskets / indices.
    udc : dict, optional
        Custom trading sessions, see sample format below.
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create
    >>> response = create(symbol="MyNewInstrument", formula="EUR=*3")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        symbol=symbol,
        formula=formula,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        currency=currency,
        time_zone=time_zone,
        holidays=holidays,
        description=description,
        type_=type_,
        basket=basket,
        udc=udc,
        extended_params=extended_params,
    )
    response = data_provider_layer.get_data(
        session, on_response, method=RequestMethod.POST
    )
    data = response.data.raw
    symbol = data.get("symbol")
    formula = data.get("formula")
    ci = CustomInstrument(symbol=symbol, formula=formula)
    ci._update(data)
    return ci
