from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class SetGpioMask (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], name: str, value_mask: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        data = {
            'name': name,
            'value_mask': value_mask
        }
        super(SetGpioMask, self).__init__(send_command, 'set_gpio_mask', data, timeout_seconds, throw_error)

class GetGpioMask (SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], name: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        data = {
            'name': name,
        }
        super(GetGpioMask, self).__init__(send_command, 'get_gpio_mask', data, timeout_seconds, throw_error)