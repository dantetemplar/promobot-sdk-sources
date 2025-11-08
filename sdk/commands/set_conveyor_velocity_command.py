from typing import Callable, Dict
from sdk.commands.abstracts.sdk_command import SdkCommand

class SetConveyorVelocityCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], velocity, timeout_seconds: float = 60.0, throw_error: bool  = True, message_bus=None):
        data = {
            'velocity': velocity
        }
        super(SetConveyorVelocityCommand, self).__init__(send_command, 'set_conveyor_velocity', data, timeout_seconds, throw_error, message_bus)