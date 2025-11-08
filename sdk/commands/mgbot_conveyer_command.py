from typing import Callable, Dict, Any
from sdk.commands.abstracts.sdk_command import SdkCommand

class MGbotConveyerCommand(SdkCommand):
    def __init__(
        self,
        send_command: Callable[[str, Dict[str, Any]], None],
        data: Dict[str, Any],
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
        message_bus=None,
    ):
        super(MGbotConveyerCommand, self).__init__(send_command, "mgbot_conveyer_control", data, timeout_seconds, throw_error, message_bus)