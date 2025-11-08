from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class PixyCamGetCoordinatesCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], signature: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        signature = {
            "signature": signature
        }
        super(PixyCamGetCoordinatesCommand, self).__init__(send_command, 'pixy_get_coordinates', signature, timeout_seconds, throw_error)