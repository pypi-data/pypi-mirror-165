# coding: utf8

from enum import Enum, unique


@unique
class RoundingType(Enum):
    CEIL = "Ceil"
    DEFAULT = "Default"
    DOWN = "Down"
    FACE_DOWN = "FaceDown"
    FACE_NEAR = "FaceNear"
    FACE_UP = "FaceUp"
    FLOOR = "Floor"
    NEAR = "Near"
    UP = "Up"
