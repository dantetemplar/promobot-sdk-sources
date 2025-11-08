from enum import Enum
from typing import Union

from sdk.commands.data import CustomModel, Pose, Point


class MoveType(Enum):
    JOINT = 0
    LINE = 1
    POINT_TO_POINT = 2
    ARC = 3


class MoveGroup(CustomModel):
    move_type: MoveType
    points: list[Union[Point, Pose]]
