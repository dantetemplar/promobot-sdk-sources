from typing import Callable
from sdk.commands.abstracts.sdk_command import SdkCommand


class MoveLinearModuleCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], distance: float, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        data = {
            "distance": distance
        }
        super(MoveLinearModuleCommand, self).__init__(send_command, 'move_linear_module', data, timeout_seconds, throw_error, message_bus)