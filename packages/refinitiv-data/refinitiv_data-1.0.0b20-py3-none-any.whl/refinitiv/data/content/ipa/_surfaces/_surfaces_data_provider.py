# coding: utf8
from typing import List

import numpy as np
import pandas as pd
from numpy import iterable

from ._models import Surface
from .._content_provider import (
    CurvesAndSurfacesRequestFactory,
    get_type_by_axis,
)
from .._enums import Axis
from ..._content_provider import ErrorParser
from ...._tools._ipa_validate import do_all_elements_have_error
from ....delivery._data._data_provider import (
    DataProvider,
    ResponseFactory,
    ContentValidator,
    Data,
    ValidatorContainer,
)


# ---------------------------------------------------------------------------
#   ContentValidator
# ---------------------------------------------------------------------------


class SurfacesContentValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = True
        content_data = data.get("content_data")
        raw_surfs = content_data.get("data")
        status = content_data.get("status", "")

        if not raw_surfs:
            is_valid = False
            data["error_code"] = 1
            data["error_message"] = "Content data is None"

        elif isinstance(raw_surfs, list) and status == "Error":
            is_valid = False
            data["error_code"] = content_data.get("code")
            data["error_message"] = content_data.get("message")
        elif isinstance(raw_surfs, list):
            is_valid = not do_all_elements_have_error(data, raw_surfs)

        return is_valid


# ---------------------------------------------------------------------------
#   Data
# ---------------------------------------------------------------------------


def parse_axis(
    universe: dict,
    x_axis: Axis,
    y_axis: Axis,
) -> (np.array, np.array, np.array):
    """
      This method parsing the surface into lists row, column and matrix

      >>> from refinitiv.data.content import ipa
      >>> definition = ipa.surfaces.eti.Definition(
      ...     underlying_definition=ipa.surfaces.eti.EtiSurfaceDefinition(
      ...         instrument_code="BNPP.PA@RIC"
      ...     ),
      ...     surface_parameters=ipa.surfaces.eti.EtiCalculationParams(
      ...         price_side=ipa.surfaces.eti.PriceSide.MID,
      ...         volatility_model=ipa.surfaces.eti.VolatilityModel.SVI,
      ...         x_axis=ipa.surfaces.eti.Axis.STRIKE,
      ...         y_axis=ipa.surfaces.eti.Axis.DATE,
      ...     ),
      ...     surface_tag="1",
      ...     surface_layout=ipa.surfaces.eti.SurfaceLayout(
      ...         format=ipa.surfaces.eti.Format.MATRIX, y_point_count=10
      ...     ),
      ... )

      This example for surface_parameters with
      x_axis = Axis.STRIKE and y_axis = Axis.DATE

      |--→ column=Y
      ↓
    row=X

      >>> surface = universe.get("surface")
      >>> surface
      ... [
      ...   [None,    '2021-08-20', '2021-09-17', '2021-12-17', '2022-03-18'],
      ...   ['25.36',  63.76680855, 76.566676686, 514160483847, 45.563136028],
      ...   ['30.432', 56.20802369, 64.051912234, 46.118622487, 41.540289743],
      ...   ['35.504', 49.91436068, 51.916645386, 41.495311424, 37.870408673],
      ... ]

      Parameters
      ----------
      universe : dict
          dict with surface
      x_axis : Axis

      y_axis : Axis

      Returns
      -------
      (np.array, np.array, np.array)
          row, column, matrix or x, y, z

      Raises
      -------
      ValueError
          If x_axis or y_axis not correct
    """

    if not x_axis or not y_axis:
        raise ValueError(
            f"Cannot parse surface "
            f"without information about x_axis={x_axis} or y_axis={y_axis}"
        )

    surface = universe.get("surface")

    # column is ['2021-08-20', '2021-09-17', '2021-12-17', '2022-03-18', '2022-06-17']
    column = surface[0][1:]
    column = np.array(column, dtype=get_type_by_axis(y_axis))

    row = []
    matrix = []

    surface = surface[1:]
    # curve is ['25.36',  63.76680855, 76.566676686, 514160483847, 41.187204258]
    for curve in surface:
        # row is '25.36'
        row.append(curve[0])
        # matrix is [63.76680855, 76.566676686, 514160483847, 41.187204258]
        matrix.append(curve[1:])

    row = np.array(row, dtype=get_type_by_axis(x_axis))
    matrix = np.array(matrix, dtype=float)

    return row, column, matrix


def create_surfaces(raw, axes_params) -> List[Surface]:
    surfaces = []

    if raw and axes_params:
        for i, universe in enumerate(raw.get("data")):
            x_axis, y_axis = axes_params[i]
            row, column, matrix = parse_axis(universe, x_axis, y_axis)
            surface = Surface(row=row, column=column, matrix=matrix)
            surfaces.append(surface)

    return surfaces


class BaseData(Data):
    def __init__(self, raw, axes_params=None):
        super().__init__(raw)
        self._axes_params = axes_params

    @property
    def df(self):
        if self._dataframe is None and self._raw:
            data = self._raw.get("data")

            if data:
                data_frame = pd.DataFrame(data)
                data_frame.set_index("surfaceTag", inplace=True)

            else:
                data_frame = pd.DataFrame([])

            if not data_frame.empty:
                data_frame = data_frame.convert_dtypes()

            self._dataframe = data_frame

        return self._dataframe


class OneSurfaceData(BaseData):
    def __init__(self, raw, axes_params):
        super().__init__(raw, axes_params)
        self._surface = None

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            surfaces = create_surfaces(self._raw, self._axes_params)
            self._surface = surfaces[0]
        return self._surface

    @property
    def df(self):
        if self._dataframe is None:
            data = {x: z for x, z in zip(self.surface.x, self.surface.z)}

            if data:
                data_frame = pd.DataFrame(data, index=self.surface.y)
            else:
                data_frame = super().df

            if not data_frame.empty:
                data_frame.fillna(pd.NA, inplace=True)
                data_frame = data_frame.convert_dtypes()

            self._dataframe = data_frame

        return self._dataframe


class SurfacesData(BaseData):
    def __init__(self, raw, axes_params):
        super().__init__(raw, axes_params)
        self._surfaces = None

    @property
    def surfaces(self) -> List[Surface]:
        if self._surfaces is None:
            self._surfaces = create_surfaces(self._raw, self._axes_params)
        return self._surfaces


# ---------------------------------------------------------------------------
#   ResponseFactory
# ---------------------------------------------------------------------------


def get_axis_params(obj, axis_params=None):
    if axis_params is None:
        axis_params = []

    if hasattr(obj, "_kwargs"):
        request_item = obj._kwargs.get("universe")

    else:
        request_item = obj

    surface_parameters = request_item.surface_parameters
    x_axis = surface_parameters._get_enum_parameter(Axis, "xAxis")
    y_axis = surface_parameters._get_enum_parameter(Axis, "yAxis")
    axis_params.append((x_axis, y_axis))
    return axis_params


class SurfaceResponseFactory(ResponseFactory):
    def create_success(self, data, *args, universe=None, **kwargs):
        response = self.response_class(is_success=True, **data)
        if universe:
            if iterable(universe):
                axes_params = []
                for definition in universe:
                    get_axis_params(definition, axes_params)
                response.data = SurfacesData(
                    raw=data.get("content_data"),
                    axes_params=axes_params,
                )
            else:
                axes_params = get_axis_params(universe)
                response.data = OneSurfaceData(
                    raw=data.get("content_data"),
                    axes_params=axes_params,
                )
        else:
            response.data = BaseData(data.get("content_data"))
        response.data._owner = response
        return response


# ---------------------------------------------------------------------------
#   DataProvider
# ---------------------------------------------------------------------------

surfaces_data_provider = DataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=SurfaceResponseFactory(),
    validator=ValidatorContainer(content_validator=SurfacesContentValidator()),
    parser=ErrorParser(),
)
