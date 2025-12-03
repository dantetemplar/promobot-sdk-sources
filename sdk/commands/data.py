from typing import Union
from pydantic import BaseModel


class CustomModel(BaseModel):
    def __init__(self, *args, **kwargs):
        fields = list(self.model_fields)
        if len(args) > len(fields):
            raise TypeError(f"Expected at most {len(fields)} positional arguments, got {len(args)}")
        kwargs |= dict(zip(fields, args))
        super().__init__(**kwargs)

    def to_dict(self) -> dict[str, Union[int, float]]:
        return self.model_dump()


class Position(CustomModel):
    x: Union[int, float]
    y: Union[int, float]
    z: Union[int, float]


class Orientation(CustomModel):
    x: Union[int, float] = 0.0
    y: Union[int, float] = 0.0
    z: Union[int, float] = 0.0
    w: Union[int, float] = 1.0


class Point3D(CustomModel):
    position: Position
    orientation: Orientation = Orientation()

    def to_dict(self) -> dict:
        return {
            'position': self.position.to_dict(),
            'orientation': self.orientation.to_dict()
        }


class Pose(CustomModel):
    position: Position
    orientation: Orientation = Orientation()
    velocity_factor: Union[int, float] = 0.1
    acceleration_factor: Union[int, float] = 0.1


class Joint(CustomModel):
    joint_name: str
    position: Union[int, float]
    velocity: Union[int, float] = 0.0


class Point(CustomModel):
    positions: list[Joint]

    def to_dict(self) -> dict[str, dict[str, Union[int, float]]]:
        position_dict: dict[str, Union[int, float]] = {}
        velocity_dict: dict[str, Union[int, float]] = {}
        for position in self.positions:
            position_dict[position.joint_name] = position.position
            velocity_dict[position.joint_name] = position.velocity
        return {'positions': position_dict, 'velocities': velocity_dict}


class JointPosition(CustomModel):
    joint: str
    position: float


class JointPositions(CustomModel):
    positions: list[JointPosition]

    def to_dict(self) -> list[dict[str, float]]:
        return [{"joint": jp.joint, "position": jp.position} for jp in self.positions]
