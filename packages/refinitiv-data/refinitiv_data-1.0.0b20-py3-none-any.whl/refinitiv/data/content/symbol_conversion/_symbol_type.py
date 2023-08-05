from enum import Enum, unique


@unique
class SymbolTypes(Enum):
    """
    Symbol types to send in request, by default "RIC" is using.
    """

    RIC = "RIC"
    ISIN = "IssueISIN"
    CUSIP = "CUSIP"
    SEDOL = "SEDOL"
    TICKER_SYMBOL = "TickerSymbol"
    OA_PERM_ID = "IssuerOAPermID"
    LIPPER_ID = "FundClassLipperID"


SYMBOL_TYPE_VALUES = tuple(t.value for t in SymbolTypes)
