from numpy import iterable

from .._ipa_content_provider import IPAContentProviderLayer
from ..._content_type import ContentType


class Definitions(IPAContentProviderLayer):
    def __init__(
        self,
        universe,
        surface_layout=None,
        extended_params=None,
    ):
        if not iterable(universe):
            universe = [universe]

        super().__init__(
            content_type=ContentType.SURFACES,
            universe=universe,
            extended_params=extended_params,
            __plural__=True,
        )
