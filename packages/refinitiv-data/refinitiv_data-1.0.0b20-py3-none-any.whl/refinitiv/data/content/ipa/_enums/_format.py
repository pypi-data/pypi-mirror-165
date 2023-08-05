# coding: utf8


from enum import Enum, unique


@unique
class Format(Enum):
    """
    The enumerate that specifies whether the calculated volatilities
    """

    LIST = "List"
    MATRIX = "Matrix"
    N_DIMENSIONAL_ARRAY = "NDimensionalArray"
