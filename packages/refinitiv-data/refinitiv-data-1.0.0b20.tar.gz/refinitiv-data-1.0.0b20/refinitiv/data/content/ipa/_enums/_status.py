# coding: utf8


from enum import Enum, unique


@unique
class Status(Enum):
    NOT_APPLICABLE = "NotApplicable"
    USER = "User"
    DATA = "Data"
    COMPUTED = "Computed"
    ERROR = "Error"
    NONE = "None"
