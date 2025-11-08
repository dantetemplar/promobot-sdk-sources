from typing import Callable, List, Dict, Optional

from sdk.commands.abstracts.sdk_command import SdkCommand
from sdk.commands.data import Joint

class MoveAnglesCommandParamsAngleInfo:
    def __init__(self, joint_name: str, angle: float, velocity: float = 0.0):
        self.name = joint_name
        self.position = angle
        self.velocity = velocity

class MoveAnglesCommand(SdkCommand):
    def __init__(
        self, 
        send_command: Callable[[str, dict], None], 
        angles: List[MoveAnglesCommandParamsAngleInfo], 
        timeout_seconds: float = 60.0, 
        throw_error: bool = True,
        velocity_factor: float = 0.1,
        acceleration_factor: float = 0.1,
        message_bus=None,
        enable_feedback: bool = False
    ):
        positions: Dict[str, float] = {}
        velocities: Dict[str, float] = {}
        
        for angle in angles:
            positions[angle.name] = angle.position
            velocities[angle.name] = 0 if angle.velocity == 0 or angle.velocity == 0.0 else angle.velocity

        data = {
            "positions": positions,
            "velocities": velocities,
            "velocity_factor": velocity_factor,
            "acceleration_factor": acceleration_factor
        }

        super(MoveAnglesCommand, self).__init__(send_command, "move_joints", data, timeout_seconds, throw_error, message_bus, enable_feedback)

    def make_command_action(self) -> None:
        print(f"[MoveAnglesCommand] Отправляем команду move_joints ID={self.command_id}")
        print(f"[MoveAnglesCommand] Данные команды: {self.command_data}")
        super().make_command_action()
        print(f"[MoveAnglesCommand] Команда отправлена успешно, ID: {self.command_id}")
