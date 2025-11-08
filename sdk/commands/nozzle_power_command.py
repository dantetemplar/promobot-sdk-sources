from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class NozzlePowerCommand (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], power: bool, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus = None):
        data = {
            "power_supply": power
        }

        super(NozzlePowerCommand, self).__init__(send_command, "nozzle_power", data, timeout_seconds, throw_error, message_bus)
