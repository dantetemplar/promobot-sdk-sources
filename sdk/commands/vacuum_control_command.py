from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class VacuumControlCommand (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], rotation: int, vacuum: bool, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        data = {}
        if rotation is not None:
            data["rotation"] = rotation
        if vacuum is not None:
            data["power_supply"] = vacuum
        super(VacuumControlCommand, self).__init__(send_command, "vacuum_control", data, timeout_seconds, throw_error, message_bus)
