# coding: utf8

from enum import Enum, unique


@unique
class RedemptionDateType(Enum):
    REDEMPTION_AT_AVERAGE_LIFE = "RedemptionAtAverageLife"
    REDEMPTION_AT_BEST_DATE = "RedemptionAtBestDate"
    REDEMPTION_AT_CALL_DATE = "RedemptionAtCallDate"
    REDEMPTION_AT_CUSTOM_DATE = "RedemptionAtCustomDate"
    REDEMPTION_AT_MAKE_WHOLE_CALL_DATE = "RedemptionAtMakeWholeCallDate"
    REDEMPTION_AT_MATURITY_DATE = "RedemptionAtMaturityDate"
    REDEMPTION_AT_NEXT_DATE = "RedemptionAtNextDate"
    REDEMPTION_AT_PAR_DATE = "RedemptionAtParDate"
    REDEMPTION_AT_PARTIAL_CALL_DATE = "RedemptionAtPartialCallDate"
    REDEMPTION_AT_PARTIAL_PUT_DATE = "RedemptionAtPartialPutDate"
    REDEMPTION_AT_PERPETUITY = "RedemptionAtPerpetuity"
    REDEMPTION_AT_PREMIUM_DATE = "RedemptionAtPremiumDate"
    REDEMPTION_AT_PUT_DATE = "RedemptionAtPutDate"
    REDEMPTION_AT_SINK_DATE = "RedemptionAtSinkDate"
    REDEMPTION_AT_WORST_DATE = "RedemptionAtWorstDate"
