from typing import Callable, Dict, Any

from sdk.commands.abstracts.sdk_command import SdkCommand

class PixyCamCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], data: Dict[str, Any], command_name, timeout_seconds: float = 60.0, throw_error: bool = True):
        super(PixyCamCommand, self).__init__(send_command, command_name, data, timeout_seconds, throw_error)
