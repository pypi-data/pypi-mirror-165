# coding: utf-8

from typing import TYPE_CHECKING

from ..._tools import create_repr
from ...delivery._data._data_provider import DataProviderLayer, BaseResponse, Data

if TYPE_CHECKING:
    from ._views import Views


class Definition(DataProviderLayer[BaseResponse[Data]]):
    """
    This class describe parameters to retrieve data for search metadata.

    Parameters
    ----------

    view : Views
        picks a subset of the data universe to search against. see Views

    Examples
    --------
    >>> from refinitiv.data.content import search
    >>> definition = search.metadata.Definition(view=search.Views.PEOPLE)
    """

    def __init__(self, view: "Views"):
        self._view = view

        from .._content_type import ContentType

        super().__init__(
            data_type=ContentType.DISCOVERY_METADATA,
            view=self._view,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="metadata",
            content=f"{{view='{self._view}'}}",
        )
