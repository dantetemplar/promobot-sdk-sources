from typing import Callable

from sdk.commands.abstracts.sdk_command import SdkCommand

class PlayAudioCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], file_name: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        data = {
            'file_name': file_name
        }
        super(PlayAudioCommand, self).__init__(send_command, 'play_audio_file', data, timeout_seconds, throw_error)