from dataclasses import dataclass, field
from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

# TODO(Victor Drobizov)
# PM-1553
# Put it in a separate file for general use:
# Position
# Orientation
# Pose

# TODO(Victor Drobizov)
# PM-1553
# Use pydentic instead of checking in __post__init___

@dataclass
class Position:
    x: float
    y: float
    z: float

    def __post_init__(self):
        for attr in ('x', 'y', 'z'):
            val = getattr(self, attr)
            if not isinstance(val, (float, int)):
                raise TypeError(f"Position.{attr} must be float, got {type(val).__name__}")

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}


@dataclass
class Orientation:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 1.0

    def __post_init__(self):
        for attr in ('x', 'y', 'z', 'w'):
            val = getattr(self, attr)
            if not isinstance(val, (float, int)):
                raise TypeError(f"Orientation.{attr} must be float, got {type(val).__name__}")

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'w': self.w}


@dataclass
class Pose:
    position: Position
    orientation: Orientation = field(default_factory=Orientation)

    def __post_init__(self):
        if not isinstance(self.position, Position):
            raise TypeError(f"Pose.position must be Position, got {type(self.position).__name__}")
        if not isinstance(self.orientation, Orientation):
            raise TypeError(f"Pose.orientation must be Orientation, got {type(self.orientation).__name__}")

    def to_dict(self):
        return {
            'position': self.position.to_dict(),
            'orientation': self.orientation.to_dict()
        }


@dataclass
class ArcMotion(SdkCommand):
    target: Pose
    center_arc: Pose
    send_command: Callable[[str, dict], None]
    step: float = 0.05
    count_point_arc: int = 50
    max_velocity_scaling_factor: float = 0.5
    max_acceleration_scaling_factor: float = 0.5
    timeout_seconds: float = 60.0
    throw_error: bool = True
    enable_feedback: bool = False

    def __post_init__(self):
        if not isinstance(self.target, Pose):
            raise TypeError(f'target must be Pose, got {type(self.target).__name__}')
        if not isinstance(self.center_arc, Pose):
            raise TypeError(f'center_arc must be Pose, got {type(self.center_arc).__name__}')
        if not callable(self.send_command):
            raise TypeError(f'send_command must be callable, got {type(self.send_command).__name__}')
        if not isinstance(self.step, float):
            raise TypeError(f'step must be float, got {type(self.step).__name__}')
        if not isinstance(self.count_point_arc, int):
            raise TypeError(f'count_point_arc must be int, got {type(self.count_point_arc).__name__}')
        if not isinstance(self.max_velocity_scaling_factor, float):
            raise TypeError(f'max_velocity_scaling_factor must be float, got {type(self.max_velocity_scaling_factor).__name__}')
        if not isinstance(self.max_acceleration_scaling_factor, float):
            raise TypeError(f'max_acceleration_scaling_factor must be float, got {type(self.max_acceleration_scaling_factor).__name__}')
        if not isinstance(self.timeout_seconds, float):
            raise TypeError(f'timeout_seconds must be float, got {type(self.timeout_seconds).__name__}')
        if not isinstance(self.throw_error, bool):
            raise TypeError(f'throw_error must be bool, got {type(self.throw_error).__name__}')

        data = {
            'target': self.target.to_dict(),
            'center_arc': self.center_arc.to_dict(),
            'step': self.step,
            'count_point_arc': self.count_point_arc,
            'max_velocity_scaling_factor': self.max_velocity_scaling_factor,
            'max_acceleration_scaling_factor': self.max_acceleration_scaling_factor,
        }

        super().__init__(self.send_command,
                         'arc_motion',
                         data,
                         self.timeout_seconds,
                         self.throw_error,
                         self.enable_feedback)
