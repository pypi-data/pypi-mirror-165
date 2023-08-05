from numpy import iterable

from ....._tools import create_repr

from ..._curves._zc_curve_types import (
    Universe,
    OptConstituents,
    CurveDefinition,
    CurveParameters,
)
from ...._content_provider import ContentProviderLayer
from ..._curves._zc_curve_request_item import ZcCurveRequestItem
from ...._content_type import ContentType
from ...._types import OptStr, ExtendedParams


class Definition(ContentProviderLayer):
    """
    Parameters
    ----------
    constituents : Constituents, optional

    curve_definition : ZcCurveDefinitions, optional

    curve_parameters : ZcCurveParameters, optional

    curve_tag : str, optional

    extended_params : dict, optional
        If necessary other parameters.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, async_mode=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
     >>> import refinitiv.data.content.ipa.curves.zc_curves as zc_curves
     >>> definition = zc_curves.Definition(
     ...     curve_definition=zc_curves.ZcCurveDefinitions(
     ...         currency="CHF",
     ...         name="CHF LIBOR Swap ZC Curve",
     ...         discounting_tenor="OIS",
     ...     ),
     ...     curve_parameters=zc_curves.ZcCurveParameters(
     ...         use_steps=True
     ...     )
     ... )
     >>> response = definition.get_data()

     Using get_data_async
     >>> import asyncio
     >>> task = definition.get_data_async()
     >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        constituents: OptConstituents = None,
        curve_definition: CurveDefinition = None,
        curve_parameters: CurveParameters = None,
        curve_tag: OptStr = None,
        extended_params: ExtendedParams = None,
    ):
        request_item = ZcCurveRequestItem(
            constituents=constituents,
            curve_definition=curve_definition,
            curve_parameters=curve_parameters,
            curve_tag=curve_tag,
        )
        super().__init__(
            content_type=ContentType.ZC_CURVES,
            universe=request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


class Definitions(ContentProviderLayer):
    """
    Parameters
    ----------
    universe : zc_curves.Definition, list of zc_curves.Definition

    extended_params : dict, optional
        If necessary other parameters.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, async_mode=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
     >>> import refinitiv.data.content.ipa.curves.zc_curves as zc_curves
     >>> definition = zc_curves.Definition(
     ...     curve_definition=zc_curves.ZcCurveDefinitions(
     ...         currency="CHF",
     ...         name="CHF LIBOR Swap ZC Curve",
     ...         discounting_tenor="OIS",
     ...     ),
     ...     curve_parameters=zc_curves.ZcCurveParameters(
     ...         use_steps=True
     ...     )
     ... )
     >>> definition = zc_curves.Definitions(universe=definition)
     >>> response = definition.get_data()

     Using get_data_async
     >>> import asyncio
     >>> task = definition.get_data_async()
     >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        universe: Universe,
        extended_params: ExtendedParams = None,
    ):
        if not iterable(universe):
            universe = [universe]

        super().__init__(
            content_type=ContentType.ZC_CURVES,
            universe=universe,
            extended_params=extended_params,
            __plural__=True,
        )

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)
