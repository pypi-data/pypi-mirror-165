# coding: utf8

from enum import Enum, unique


@unique
class DocClause(Enum):
    CUM_RESTRUCT03 = "CumRestruct03"
    CUM_RESTRUCT14 = "CumRestruct14"
    EX_RESTRUCT03 = "ExRestruct03"
    EX_RESTRUCT14 = "ExRestruct14"
    MOD_MOD_RESTRUCT03 = "ModModRestruct03"
    MOD_MOD_RESTRUCT14 = "ModModRestruct14"
    MODIFIED_RESTRUCT03 = "ModifiedRestruct03"
    MODIFIED_RESTRUCT14 = "ModifiedRestruct14"
    NONE = "None"
