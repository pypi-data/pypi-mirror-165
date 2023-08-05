from typing import Union, Iterable

from ._asset_class import AssetClass
from ._asset_state import AssetState
from ._country_code import CountryCode
from ._symbol_type import SymbolTypes, SYMBOL_TYPE_VALUES
from .._content_provider import ContentProviderLayer
from ..search import Views
from ..._tools import make_convert_to_enum, ArgsParser, make_parse_enum


def make_symbology_enum_parser(enum_class, can_be_lower=True):
    parser = make_parse_enum(enum_class, can_be_lower)

    def _parser(value):
        lower_values = {
            name.lower(): item for name, item in enum_class.__members__.items()
        }
        if isinstance(value, str) and value.lower() in lower_values:
            value = lower_values[value.lower()]
        return parser(value)

    return ArgsParser(_parser)


search_all_category_by_asset_class = {
    AssetClass.COMMODITIES: "Commodities",
    AssetClass.EQUITY_OR_INDEX_OPTIONS: "Options",
    AssetClass.BOND_AND_STIR_FUTURES_AND_OPTIONS: "Exchange-Traded Rates",
    AssetClass.EQUITIES: "Equities",
    AssetClass.EQUITY_INDEX_FUTURES: "Futures",
    AssetClass.FUNDS: "Funds",
    AssetClass.BONDS: "Bond Pricing",
    AssetClass.FX_AND_MONEY: "FX & Money",
}

rcsasset_category_genealogy_by_asset_class = {
    AssetClass.WARRANTS: "A:AA",
    AssetClass.CERTIFICATES: "A:6N",
    AssetClass.INDICES: "I:17",
    AssetClass.RESERVE_CONVERTIBLE: "A:LE",
    AssetClass.MINI_FUTURE: "A:P6",
}


def _transform_to_string(values: Iterable, category: dict) -> str:
    string_of_values = ""
    for value in values:
        request_value = category[value]
        string_of_values = f"{string_of_values} '{request_value}'"
    return string_of_values


def _create_asset_class_request_strings(asset_class: list) -> tuple:
    search_all_category_values = filter(
        lambda x: x in search_all_category_by_asset_class, asset_class
    )
    rcs_asset_category_values = filter(
        lambda x: x in rcsasset_category_genealogy_by_asset_class, asset_class
    )

    search_all_category_string_values = _transform_to_string(
        search_all_category_values, search_all_category_by_asset_class
    )

    search_all_rcs_asset_category_string_values = _transform_to_string(
        rcs_asset_category_values, rcsasset_category_genealogy_by_asset_class
    )

    search_all_category_string = ""
    rcs_asset_category_string = ""

    if search_all_category_string_values:
        search_all_category_string = (
            f"SearchAllCategoryv3 in ({search_all_category_string_values})"
        )

    if search_all_rcs_asset_category_string_values:
        rcs_asset_category_string = f"RCSAssetCategoryGenealogy in ({search_all_rcs_asset_category_string_values})"

    return search_all_category_string, rcs_asset_category_string


def _prepare_filter(
    asset_state: AssetState, asset_class: Union[list, AssetClass]
) -> str:
    asset_state = asset_state or AssetState.ACTIVE

    if asset_state is AssetState.ACTIVE:
        ret_val = "AssetState eq 'AC'"
    else:
        ret_val = "(AssetState ne 'AC' and AssetState ne null)"

    if asset_class and not isinstance(asset_class, list):
        asset_class = [asset_class]

    if asset_class:
        search_all_category, rcs_asset_category = _create_asset_class_request_strings(
            asset_class
        )

        if search_all_category and rcs_asset_category:
            ret_val = f"{ret_val} and ({search_all_category} or {rcs_asset_category})"
        else:
            ret_val = f"{ret_val} and ({search_all_category}{rcs_asset_category})"

    return ret_val


class SymbologyContentProviderLayer(ContentProviderLayer):
    def __init__(self, **kwargs):
        from .._content_type import ContentType

        asset_state = kwargs.get("asset_state")
        if asset_state and not isinstance(asset_state, AssetState):
            asset_state = convert_asset_state_to_enum(asset_state)
        asset_class = kwargs.get("asset_class")
        if asset_class and not isinstance(asset_class, AssetClass):
            asset_class = convert_asset_class_to_enum(asset_class)
        filter_ = _prepare_filter(asset_state, asset_class)

        preferred_country_code = kwargs.get("preferred_country_code")
        if preferred_country_code:
            preferred_country_code = f"RCSExchangeCountry eq '{country_code_arg_parser.get_str(preferred_country_code)}'"

        from_symbol_type = kwargs.get("from_symbol_type")
        if from_symbol_type and from_symbol_type != "_AllUnique":
            from_symbol_type = symbol_types_arg_parser.get_str(from_symbol_type)

        select = ["DocumentTitle"]
        to_symbol_types = kwargs.get("to_symbol_types")
        if to_symbol_types is SYMBOL_TYPE_VALUES:
            select.extend(to_symbol_types)
        elif isinstance(to_symbol_types, list):
            select.extend(map(symbol_types_arg_parser.get_str, to_symbol_types))
        elif to_symbol_types:
            select.append(symbol_types_arg_parser.get_str(to_symbol_types))

        select = ",".join(select)

        symbols = kwargs.get("symbols")
        if isinstance(symbols, list):
            symbols = ",".join(symbols)

        super().__init__(
            content_type=ContentType.DISCOVERY_LOOKUP,
            **{
                "view": Views.SEARCH_ALL,
                "terms": symbols,
                "scope": from_symbol_type,
                "select": select,
                "extended_params": kwargs.get("extended_params"),
                "closure": kwargs.get("closure"),
                "filter": filter_,
                "boost": preferred_country_code,
            },
        )


country_code_arg_parser = make_symbology_enum_parser(CountryCode)
symbol_types_arg_parser = make_symbology_enum_parser(SymbolTypes)
convert_asset_class_to_enum = make_convert_to_enum(AssetClass)
convert_asset_state_to_enum = make_convert_to_enum(AssetState)
