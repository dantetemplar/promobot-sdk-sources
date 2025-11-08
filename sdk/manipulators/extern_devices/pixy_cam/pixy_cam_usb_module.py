from sdk.manipulators.extern_devices.pixy_cam.pixy_cam_module_base import PixyCamModuleBase


class PixyCamUsbModule(PixyCamModuleBase):
    def __init__(self, message_bus, run_async, parent):
        self.message_bus = message_bus
        self._run_async = run_async
        self._parent = parent
        self.specific_command = None
        self._command_name = 'pixy_cam_usb_control'
    

    def line_all_features_async(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "lineAllFeatures", "max": max_items}, timeout_seconds, throw_error)

    async def line_all_features_async_await(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.line_all_features_usb, max_items, timeout_seconds, throw_error)

    def line_all_features_usb(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.line_all_features_async(max_items, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result


    def line_main_features_async(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "lineMainFeatures", "max": max_items}, timeout_seconds, throw_error)

    async def line_main_features_async_await(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.line_main_features_usb, max_items, timeout_seconds, throw_error)

    def line_main_features_usb(self, max_items: int = 100, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.line_main_features_async(max_items, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result


    def get_frame_size_async(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "getFrameSize"}, timeout_seconds, throw_error)

    async def get_frame_size_async_await(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.get_frame_size_usb, timeout_seconds, throw_error)

    def get_frame_size_usb(self, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.get_frame_size_async(timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result


    def set_servos_async(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"cmd": "setServos", "s0": s0, "s1": s1}, timeout_seconds, throw_error)

    async def set_servos_async_await(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_servos_usb, s0, s1, timeout_seconds, throw_error)

    def set_servos_usb(self, s0: int, s1: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        command = self.set_servos_async(s0, s1, timeout_seconds, throw_error)
        command.make_command_action()
        result = command.result()
        self.specific_command = None
        return result
