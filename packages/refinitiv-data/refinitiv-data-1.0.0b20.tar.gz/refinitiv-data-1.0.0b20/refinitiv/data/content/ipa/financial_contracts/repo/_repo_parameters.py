# coding: utf8


from typing import Optional

from .._instrument_definition import ObjectDefinition


class RepoParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    coupon_paid_at_horizon : bool, optional
        Flag that defines whether coupons paid at horizon.  this has no impact on
        pricing.
    haircut_rate_percent : float, optional
        The reduction applied to the value of an underlying asset for purposes of
        calculating a repo collateral. the value is computed as [(initialmarginpercent -
        100) / initialmarginpercent] and expressed in percentages. either haircut or
        initial marging field can be bet. optional. by default it is computed from
        initialmarginpercent.
    initial_margin_percent : float, optional
        The initial market value of collateral expressed as a percentage of the purchase
        price of the underlying asset. either haircutratepercent or initialmarginpercent
        can be overriden. optional. default value is 100.
    purchase_price : float, optional
        Purchase price of the asset. this parameter can be used to solve repurchaseprice
        from this purchaseprice value. optional. by default it is computed from net
        present value and initial margin.
    repurchase_price : float, optional
        Repurchase price of the asset. this parameter can be used to solve purchaseprice
        from this repurchaseprice value. optional. by default it is computed from
        underlying end price, or solved from purchaseprice and repo rate.
    """

    def __init__(
        self,
        coupon_paid_at_horizon: Optional[bool] = None,
        haircut_rate_percent: Optional[float] = None,
        initial_margin_percent: Optional[float] = None,
        purchase_price: Optional[float] = None,
        repurchase_price: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.coupon_paid_at_horizon = coupon_paid_at_horizon
        self.haircut_rate_percent = haircut_rate_percent
        self.initial_margin_percent = initial_margin_percent
        self.purchase_price = purchase_price
        self.repurchase_price = repurchase_price

    @property
    def coupon_paid_at_horizon(self):
        """
        Flag that defines whether coupons paid at horizon.  this has no impact on
        pricing.
        :return: bool
        """
        return self._get_parameter("couponPaidAtHorizon")

    @coupon_paid_at_horizon.setter
    def coupon_paid_at_horizon(self, value):
        self._set_parameter("couponPaidAtHorizon", value)

    @property
    def haircut_rate_percent(self):
        """
        The reduction applied to the value of an underlying asset for purposes of
        calculating a repo collateral. the value is computed as [(initialmarginpercent -
        100) / initialmarginpercent] and expressed in percentages. either haircut or
        initial marging field can be bet. optional. by default it is computed from
        initialmarginpercent.
        :return: float
        """
        return self._get_parameter("haircutRatePercent")

    @haircut_rate_percent.setter
    def haircut_rate_percent(self, value):
        self._set_parameter("haircutRatePercent", value)

    @property
    def initial_margin_percent(self):
        """
        The initial market value of collateral expressed as a percentage of the purchase
        price of the underlying asset. either haircutratepercent or initialmarginpercent
        can be overriden. optional. default value is 100.
        :return: float
        """
        return self._get_parameter("initialMarginPercent")

    @initial_margin_percent.setter
    def initial_margin_percent(self, value):
        self._set_parameter("initialMarginPercent", value)

    @property
    def purchase_price(self):
        """
        Purchase price of the asset. this parameter can be used to solve repurchaseprice
        from this purchaseprice value. optional. by default it is computed from net
        present value and initial margin.
        :return: float
        """
        return self._get_parameter("purchasePrice")

    @purchase_price.setter
    def purchase_price(self, value):
        self._set_parameter("purchasePrice", value)

    @property
    def repurchase_price(self):
        """
        Repurchase price of the asset. this parameter can be used to solve purchaseprice
        from this repurchaseprice value. optional. by default it is computed from
        underlying end price, or solved from purchaseprice and repo rate.
        :return: float
        """
        return self._get_parameter("repurchasePrice")

    @repurchase_price.setter
    def repurchase_price(self, value):
        self._set_parameter("repurchasePrice", value)
