# coding: utf8

from typing import Optional, TYPE_CHECKING, List

from ...._types import Strings, ExtendedParams
from ._swap_definition import SwapInstrumentDefinition
from .._base_definition import BaseDefinition

if TYPE_CHECKING:
    from . import LegDefinition, PricingParameters


class Definition(BaseDefinition):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tenor: Optional[str] = None,
        legs: Optional[List["LegDefinition"]] = None,
        is_non_deliverable: Optional[bool] = None,
        settlement_ccy: Optional[str] = None,
        start_tenor: Optional[str] = None,
        template: Optional[str] = None,
        fields: Optional[Strings] = None,
        pricing_parameters: Optional["PricingParameters"] = None,
        extended_params: ExtendedParams = None,
    ):
        definition = SwapInstrumentDefinition(
            legs=legs,
            end_date=end_date,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            is_non_deliverable=is_non_deliverable,
            settlement_ccy=settlement_ccy,
            start_date=start_date,
            start_tenor=start_tenor,
            template=template,
            tenor=tenor,
            trade_date=trade_date,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
