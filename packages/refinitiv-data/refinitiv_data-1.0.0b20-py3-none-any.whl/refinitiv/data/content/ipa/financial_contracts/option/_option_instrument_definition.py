# coding: utf8

from typing import Optional

from ._enums import BuySell, CallPut, ExerciseStyle, UnderlyingType, SettlementType
from ._eti import (
    EtiUnderlyingDefinition,
    EtiBinaryDefinition,
    EtiBarrierDefinition,
    EtiDefinition,
    EtiCbbcDefinition,
    EtiDoubleBarriersDefinition,
    EtiFixingInfo,
)
from ._fx import (
    FxDefinition,
    FxDualCurrencyDefinition,
    FxDoubleBarrierDefinition,
    FxDoubleBinaryDefinition,
    FxForwardStart,
)
from ._option_definition import OptionDefinition
from ._models import InputFlow


class OptionInstrumentDefinition(EtiDefinition, FxDefinition, OptionDefinition):
    def __init__(
        self,
        asian_definition: Optional[EtiFixingInfo] = None,
        barrier_definition: Optional[EtiBarrierDefinition] = None,
        binary_definition: Optional[EtiBinaryDefinition] = None,
        buy_sell: Optional[BuySell] = None,
        call_put: Optional[CallPut] = None,
        cbbc_definition: Optional[EtiCbbcDefinition] = None,
        deal_contract: Optional[int] = None,
        delivery_date: Optional[str] = None,
        double_barrier_definition: Optional[FxDoubleBarrierDefinition] = None,
        double_barriers_definition: Optional[EtiDoubleBarriersDefinition] = None,
        double_binary_definition: Optional[FxDoubleBinaryDefinition] = None,
        dual_currency_definition: Optional[FxDualCurrencyDefinition] = None,
        end_date: Optional[str] = None,
        end_date_time: Optional[str] = None,
        exercise_style: Optional[ExerciseStyle] = None,
        forward_start_definition: Optional[FxForwardStart] = None,
        instrument_code: Optional[str] = None,
        instrument_tag: Optional[str] = None,
        lot_size: Optional[float] = None,
        notional_amount: Optional[float] = None,
        notional_ccy: Optional[str] = None,
        payments: Optional[InputFlow] = None,
        settlement_ccy: Optional[str] = None,
        settlement_type: Optional[SettlementType] = None,
        start_date: Optional[str] = None,
        strike: Optional[float] = None,
        tenor: Optional[str] = None,
        time_zone_offset: Optional[int] = None,
        underlying_definition: Optional[EtiUnderlyingDefinition] = None,
        underlying_type: Optional[UnderlyingType] = None,
    ):
        super().__init__(
            asian_definition=asian_definition,
            barrier_definition=barrier_definition,
            binary_definition=binary_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            cbbc_definition=cbbc_definition,
            deal_contract=deal_contract,
            delivery_date=delivery_date,
            double_barrier_definition=double_barrier_definition,
            double_barriers_definition=double_barriers_definition,
            double_binary_definition=double_binary_definition,
            dual_currency_definition=dual_currency_definition,
            end_date=end_date,
            end_date_time=end_date_time,
            exercise_style=exercise_style,
            forward_start_definition=forward_start_definition,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            lot_size=lot_size,
            notional_amount=notional_amount,
            notional_ccy=notional_ccy,
            payments=payments,
            settlement_ccy=settlement_ccy,
            settlement_type=settlement_type,
            start_date=start_date,
            strike=strike,
            tenor=tenor,
            time_zone_offset=time_zone_offset,
            underlying_definition=underlying_definition,
            underlying_type=underlying_type,
        )
