from typing import Callable
from sdk.commands.abstracts.sdk_command import SdkCommand

class CalibrateControllerCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super(CalibrateControllerCommand, self).__init__(send_command, 'calibration_linear_module', 'None', timeout_seconds, throw_error, message_bus)
