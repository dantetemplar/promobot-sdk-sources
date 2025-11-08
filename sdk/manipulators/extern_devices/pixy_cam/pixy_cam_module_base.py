from typing import Callable, Dict, Any, Optional
from sdk.commands.pixy_cam_command import PixyCamCommand
from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC


class PixyCamModuleBase:
    def __init__(self, message_bus, run_async: Callable, parent, command_name: str):
        self.message_bus = message_bus
        self._run_async = run_async
        self._parent = parent
        self._command_name = command_name
        self.specific_command: Optional[Any] = None

    def _create_command(self, data: Dict[str, Any], timeout_seconds: float = 60.0, throw_error: bool = True) -> PixyCamCommand:
        command = self.specific_command = PixyCamCommand(
            self.message_bus.publish,
            data,
            self._command_name,
            timeout_seconds,
            throw_error
        )
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command = command
        self._parent.specific_command = command
        return command
    
    def get_blocks_async(self, sigmap: int = 0xFF, max_blocks: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getBlocks", "sigmap": sigmap, "max_blocks": max_blocks}, timeout_seconds, throw_error)

    async def get_blocks_async_await(self, sigmap: int = 0xFF, max_blocks: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_blocks, sigmap, max_blocks, timeout_seconds, throw_error)

    def get_blocks(self, sigmap: int = 0xFF, max_blocks: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_blocks_async(sigmap, max_blocks, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    
    
    def get_rgb_async(self, x: int, y: int, saturate: bool = False, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getRGB", "x": x, "y": y, "saturate": int(saturate)}, timeout_seconds, throw_error)

    async def get_rgb_async_await(self, x: int, y: int, saturate: bool = False, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_rgb, x, y, saturate, timeout_seconds, throw_error)

    def get_rgb(self, x: int, y: int, saturate: bool = False, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_rgb_async(x, y, saturate, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    
    def set_lamp_async(self, upper: bool, lower: bool, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "setLamp", "upper": int(upper), "lower": int(lower)}, timeout_seconds, throw_error)

    async def set_lamp_async_await(self, upper: bool, lower: bool, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_lamp, upper, lower, timeout_seconds, throw_error)

    def set_lamp(self, upper: bool, lower: bool, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.set_lamp_async(upper, lower, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result