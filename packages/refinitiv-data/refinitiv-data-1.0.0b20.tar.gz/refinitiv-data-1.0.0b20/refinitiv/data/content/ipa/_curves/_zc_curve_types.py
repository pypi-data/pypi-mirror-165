from typing import Iterable, Union, Optional

from ..._types import Strings

Steps = Union[Iterable["Step"]]
Turns = Union[Iterable["Turn"]]
OptConstituents = Optional["Constituents"]
CurveDefinition = Optional["ZcCurveDefinitions"]
CurveParameters = Optional["ZcCurveParameters"]
Universe = Union["zc_curve.Definition", Iterable["zc_curve.Definition"]]
Outputs = Union[Strings, Iterable["ZcCurvesOutputs"]]
