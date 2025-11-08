from sdk.manipulators.extern_devices.pixy_cam.pixy_cam_module_base import PixyCamModuleBase


class PixyCamUartModule(PixyCamModuleBase):
    def __init__(self, message_bus, run_async, parent):
        self.message_bus = message_bus
        self._run_async = run_async
        self._parent = parent
        self.specific_command = None
        self._command_name = 'pixy_cam_uart_control'


    def get_version_async(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getVersion"}, timeout_seconds, throw_error)

    async def get_version_async_await(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_version, timeout_seconds, throw_error)

    def get_version(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_version_async(timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    

    def get_resolution_async(self, type: int = 0, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getResolution", "type": type}, timeout_seconds, throw_error)

    async def get_resolution_async_await(self, type: int = 0, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_resolution_uart, type, timeout_seconds, throw_error)

    def get_resolution_uart(self, type: int = 0, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_resolution_async(type, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    

    def get_fps_async(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getFPS"}, timeout_seconds, throw_error)

    async def get_fps_async_await(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_fps_uart, timeout_seconds, throw_error)

    def get_fps_uart(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_fps_async(timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    

    def set_camera_brightness_async(self, brightness: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "setCameraBrightness", "brightness": brightness}, timeout_seconds, throw_error)

    async def set_camera_brightness_async_await(self, brightness: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_camera_brightness_uart, brightness, timeout_seconds, throw_error)

    def set_camera_brightness_uart(self, brightness: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.set_camera_brightness_async(brightness, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    

    def set_servos_async(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "setServos", "s0": s0, "s1": s1}, timeout_seconds, throw_error)

    async def set_servos_async_await(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_servos_uart, s0, s1, timeout_seconds, throw_error)

    def set_servos_uart(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.set_servos_async(s0, s1, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
    

    def set_led_async(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "setLED", "r": r, "g": g, "b": b}, timeout_seconds, throw_error)

    async def set_led_async_await(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_led_uart, r, g, b, timeout_seconds, throw_error)

    def set_led_uart(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.set_led_async(r, g, b, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
