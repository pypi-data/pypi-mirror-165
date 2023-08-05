# coding: utf8


from typing import Optional

from .._enums import PremiumSettlementType
from .._object_definition import ObjectDefinition


class InputFlow(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    amount : float, optional

    premium_settlement_type : PremiumSettlementType, optional
        The cash settlement type of the option premium -spot -forward
    currency : str, optional

    date : str, optional

    """

    def __init__(
        self,
        amount: Optional[float] = None,
        premium_settlement_type: Optional[PremiumSettlementType] = None,
        currency: Optional[str] = None,
        date: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.amount = amount
        self.premium_settlement_type = premium_settlement_type
        self.currency = currency
        self.date = date

    @property
    def premium_settlement_type(self):
        """
        The cash settlement type of the option premium -spot -forward
        :return: enum PremiumSettlementType
        """
        return self._get_enum_parameter(PremiumSettlementType, "premiumSettlementType")

    @premium_settlement_type.setter
    def premium_settlement_type(self, value):
        self._set_enum_parameter(PremiumSettlementType, "premiumSettlementType", value)

    @property
    def amount(self):
        """
        :return: float
        """
        return self._get_parameter("amount")

    @amount.setter
    def amount(self, value):
        self._set_parameter("amount", value)

    @property
    def currency(self):
        """
        :return: str
        """
        return self._get_parameter("currency")

    @currency.setter
    def currency(self, value):
        self._set_parameter("currency", value)

    @property
    def date(self):
        """
        :return: str
        """
        return self._get_parameter("date")

    @date.setter
    def date(self, value):
        self._set_parameter("date", value)
