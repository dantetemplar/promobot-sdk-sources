from enum import Enum
from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class MoveCoordinatesParamsPosition:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

class MoveCoordinatesParamsOrientation:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w


class PlannerType(Enum):
    PTP: str = 'PTP'
    LIN: str = 'LIN'


class MoveCoordinatesParams:
    def __init__(self,
                 position: MoveCoordinatesParamsPosition,
                 orientation: MoveCoordinatesParamsOrientation,
                 max_velocity_scaling_factor: float,
                 max_acceleration_scaling_factor: float,
                 planner_type: PlannerType = PlannerType.LIN):
        self.position = position
        self.orientation = orientation
        self.max_velocity_scaling_factor = max_velocity_scaling_factor
        self.max_acceleration_scaling_factor = max_acceleration_scaling_factor
        self.planner_type = planner_type

    def get_command_data(self):
        return {
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z
            },
            "orientation": {
                "x": self.orientation.x,
                "y": self.orientation.y,
                "z": self.orientation.z,
                "w": self.orientation.w
            },
            "velocity_factor": self.max_velocity_scaling_factor,
            "acceleration_factor": self.max_acceleration_scaling_factor,
            'type': self.planner_type.value
        }

class MoveCoordinatesCommand (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], parameters: MoveCoordinatesParams, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super(MoveCoordinatesCommand, self).__init__(send_command, "set_coordinates", parameters.get_command_data(), timeout_seconds, throw_error, message_bus)