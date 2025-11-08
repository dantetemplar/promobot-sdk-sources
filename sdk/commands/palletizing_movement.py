from dataclasses import dataclass
from typing import Any, Callable
from pydantic import Field

from sdk.commands.abstracts.sdk_command import SdkCommand
from sdk.commands.data import Pose, Orientation


@dataclass
class PaletizingMovement(SdkCommand):
    def __init__(self,
                 target_point: Pose,
                 hold_orientation: Orientation = Field(default_factory=Orientation),
                 use_orientation: bool = False,
                 step: float = 0.05,
                 count_point: int = 50,
                 max_velocity_scaling_factor: float = 0.1,
                 max_acceleration_scaling_factor: float = 0.1,
                 send_command: Callable[[str, dict], None] = False,
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True, message_bus = None, enable_feedback: bool = False):
        data = {
            'target_point': target_point.to_dict(),
            'orientation': hold_orientation.to_dict(),
            'use_orientation': use_orientation,
            'step': step,
            'count_point': count_point,
            'max_velocity_scaling_factor': max_velocity_scaling_factor,
            'max_acceleration_scaling_factor': max_acceleration_scaling_factor,
        }

        super(PaletizingMovement,self).__init__(send_command,
                                                'palletizing_movement',
                                                data, timeout_seconds, throw_error, message_bus)
