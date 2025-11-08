from typing import Optional, Dict, Any
from sdk.promise import Promise

from sdk.commands.mgbot_conveyer_command import MGbotConveyerCommand
from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC, MGBOT_TOPIC

class MGbotConveyer:
    def __init__(self, message_bus, run_async, parent):
        self.message_bus = message_bus
        self._run_async = run_async
        self._parent = parent
        self.specific_command = None
        self.mgbot_promise: Optional[Promise] = None
        self.last_sensor_data: Optional[Dict[str, Any]] = None

    def _create_command(self, data: dict, timeout_seconds: float = 60.0, throw_error: bool = True) -> MGbotConveyerCommand:
        command = MGbotConveyerCommand(
            self.message_bus.publish,
            data,
            timeout_seconds,
            throw_error
        )
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.message_bus.subscribe(MGBOT_TOPIC)
        self.specific_command = command
        self._parent.specific_command = command

        self.mgbot_promise = Promise(timeout_seconds, throw_error)
        promise = self.mgbot_promise

        return command, promise
    
    def set_buzz_tone_async(self, freq: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"Buz": freq}, timeout_seconds, throw_error)

    async def set_buzz_tone_async_await(self, freq: int, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        await self._run_async(self.set_buzz_tone, freq, timeout_seconds, throw_error)

    def set_buzz_tone(self, freq: int, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        command, promise = self.set_buzz_tone_async(freq, timeout_seconds, throw_error)
        command.make_command_action()
        command.result()
        self.specific_command = None
    
    def set_speed_motors_async(self, speed: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"SpeedMotors": speed}, timeout_seconds, throw_error)

    async def set_speed_motors_async_await(self, speed: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_speed_motors, speed, timeout_seconds, throw_error)

    def set_speed_motors(self, speed: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        cmd, promise = self.set_speed_motors_async(speed, timeout_seconds, throw_error)
        cmd.make_command_action()
        cmd.result()
        self.specific_command = None

    def set_servo_angle_async(self, angle: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"Servo": angle}, timeout_seconds, throw_error)

    async def set_servo_angle_async_await(self, angle: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_servo_angle, angle, timeout_seconds, throw_error)

    def set_servo_angle(self, angle: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        cmd, promise = self.set_servo_angle_async(angle, timeout_seconds, throw_error)
        cmd.make_command_action()
        cmd.result()
        self.specific_command = None

    def set_led_color_async(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"Led": {"R": r, "G": g, "B": b}}, timeout_seconds, throw_error)

    async def set_led_color_async_await(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.set_led_color, r, g, b, timeout_seconds, throw_error)

    def set_led_color(self, r: int, g: int, b: int, timeout_seconds: float = 60.0, throw_error: bool = True):
        cmd, promise = self.set_led_color_async(r, g, b, timeout_seconds, throw_error)
        cmd.make_command_action()
        cmd.result()
        self.specific_command = None

    def display_text_async(self, message: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"Text": message}, timeout_seconds, throw_error)

    async def display_text_async_await(self, message: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        await self._run_async(self.display_text, message, timeout_seconds, throw_error)

    def display_text(self, message: str, timeout_seconds: float = 60.0, throw_error: bool = True):
        cmd, promise = self.display_text_async(message, timeout_seconds, throw_error)
        cmd.make_command_action()
        cmd.result()
        self.specific_command = None

    def get_sensors_data_async(self, enabled: bool = True, timeout_seconds: float = 60.0, throw_error: bool = True):
        return self._create_command({"Sensors": 1 if enabled else 0}, timeout_seconds, throw_error)

    async def get_sensors_data_async_await(self, enabled: bool = True, timeout_seconds: float = 60.0, throw_error: bool = True):
        return await self._run_async(self.get_sensors_data, enabled, timeout_seconds, throw_error)

    def get_sensors_data(self, enabled: bool = True, timeout_seconds: float = 60.0, throw_error: bool = True) -> Dict[str, Any]:
        cmd, promise = self.get_sensors_data_async(enabled, timeout_seconds, throw_error)
        cmd.make_command_action()
        cmd.result()
        promise.result()
        self.specific_command = None
        
        try:
            return self.last_sensor_data
        finally:
            self.sensor_data_promise = None