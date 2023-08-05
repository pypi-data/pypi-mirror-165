from enum import Enum, unique


@unique
class SortOrder(Enum):
    old_to_new = "oldToNew"
    new_to_old = "newToOld"


_SORT_ORDER_VALUES = [k.value for k in SortOrder]
