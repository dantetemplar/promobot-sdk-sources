from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class GripperControlCommand (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], rotation: int, gripper: int, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        data = {}
        if rotation is not None:
            data["rotation"] = rotation
        if gripper is not None:
            data["gripper"] = gripper

        super(GripperControlCommand, self).__init__(send_command, "gripper_control", data, timeout_seconds, throw_error, message_bus)
