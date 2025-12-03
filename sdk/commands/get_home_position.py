from typing import Callable, Dict, Any

from sdk.commands.abstracts.sdk_command import SdkCommand

class GetHomePosition(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True):
        super(GetHomePosition, self).__init__(send_command, 'get_home_position', 'None', timeout_seconds, throw_error)