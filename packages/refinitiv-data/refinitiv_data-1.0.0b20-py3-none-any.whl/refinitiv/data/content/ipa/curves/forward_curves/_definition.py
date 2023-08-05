from numpy import iterable

from ....._tools import create_repr
from ..._curves._forward_curve_request_item import ForwardCurveRequestItem
from ..._curves._forward_curve_types import (
    OptStr,
    Universe,
    ExtendedParams,
    CurveDefinition,
    ForwardCurveDefinitions,
    CurveParameters,
)
from ...._content_provider import ContentProviderLayer
from ...._content_type import ContentType


class Definition(ContentProviderLayer):
    """
    Parameters
    ----------
    curve_definition : SwapZcCurveDefinition, optional

    curve_parameters : SwapZcCurveParameters, optional

    forward_curve_definitions : list of ForwardCurveDefinition, optional

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
     >>> import refinitiv.data.content.ipa.curves.forward_curves as forward_curves
     >>> definition = forward_curves.Definition(
     ...     curve_definition=forward_curves.SwapZcCurveDefinition(
     ...         currency="EUR",
     ...         index_name="EURIBOR",
     ...         name="EUR EURIBOR Swap ZC Curve",
     ...         discounting_tenor="OIS",
     ...     ),
     ...     forward_curve_definitions=[
     ...         forward_curves.ForwardCurveDefinition(
     ...             index_tenor="3M",
     ...             forward_curve_tag="ForwardTag",
     ...             forward_start_date="2021-02-01",
     ...             forward_curve_tenors=[
     ...                 "0D",
     ...                 "1D",
     ...                 "2D",
     ...                 "3M",
     ...                 "6M",
     ...                 "9M",
     ...                 "1Y",
     ...                 "2Y",
     ...                 "3Y",
     ...                 "4Y",
     ...                 "5Y",
     ...                 "6Y",
     ...                 "7Y",
     ...                 "8Y",
     ...                 "9Y",
     ...                 "10Y",
     ...                 "15Y",
     ...                 "20Y",
     ...                 "25Y"
     ...             ]
     ...         )
     ...     ]
     ... )
     >>> response = definition.get_data()

     Using get_data_async
     >>> import asyncio
     >>> task = definition.get_data_async()
     >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        curve_definition: CurveDefinition = None,
        forward_curve_definitions: ForwardCurveDefinitions = None,
        curve_parameters: CurveParameters = None,
        curve_tag: OptStr = None,
        extended_params: ExtendedParams = None,
    ):
        request_item = ForwardCurveRequestItem(
            curve_definition=curve_definition,
            forward_curve_definitions=forward_curve_definitions,
            curve_parameters=curve_parameters,
            curve_tag=curve_tag,
        )
        super().__init__(
            content_type=ContentType.FORWARD_CURVE,
            universe=request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


class Definitions(ContentProviderLayer):
    """
    Parameters
    ----------
    universe : forward_curves.Definition, list of forward_curves.Definition

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
     >>> import refinitiv.data.content.ipa.curves.forward_curves as forward_curves
     >>>
     >>> forward_curve_definition = forward_curves.Definition(
     ...     curve_definition=forward_curves.SwapZcCurveDefinition(
     ...         currency="EUR",
     ...         index_name="EURIBOR",
     ...         name="EUR EURIBOR Swap ZC Curve",
     ...         discounting_tenor="OIS",
     ...     ),
     ...     forward_curve_definitions=[
     ...         forward_curves.ForwardCurveDefinition(
     ...             index_tenor="3M",
     ...             forward_curve_tag="ForwardTag",
     ...             forward_start_date="2021-02-01",
     ...             forward_curve_tenors=[
     ...                 "0D",
     ...                 "1D",
     ...                 "2D",
     ...                 "3M",
     ...                 "6M",
     ...                 "9M",
     ...                 "1Y",
     ...                 "2Y",
     ...                 "3Y",
     ...                 "4Y",
     ...                 "5Y",
     ...                 "6Y",
     ...                 "7Y",
     ...                 "8Y",
     ...                 "9Y",
     ...                 "10Y",
     ...                 "15Y",
     ...                 "20Y",
     ...                 "25Y"
     ...             ]
     ...         )
     ...     ]
     ... )
     >>> definition = forward_curves.Definitions(
     ...     universe=[forward_curve_definition],
     ... )
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
            content_type=ContentType.FORWARD_CURVE,
            universe=universe,
            extended_params=extended_params,
            __plural__=True,
        )

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)
