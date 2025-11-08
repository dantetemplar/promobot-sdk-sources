from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass
from sdk.commands.abstracts.sdk_command import SdkCommand
from sdk.commands.base_command import CommandParams

# Константы для состояний манипулятора теперь определены в sdk.utils.enums.ManipulatorState

class SetStateCommand(SdkCommand):
    def __init__(self, state_id: int, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super().__init__(
            send_command,
            "set_state",
            {"id": state_id},
            timeout_seconds,
            throw_error,
            message_bus
        )


class RunProgramJsonCommand(SdkCommand):
    def __init__(self, name: str, program_json: Dict[str, Any], send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None, enable_feedback: bool = False):
        super().__init__(
            send_command,
            "play_program_json",
            {
                "name": name,
                "json": program_json
            },
            timeout_seconds,
            throw_error,
            message_bus,
            enable_feedback
        )


class RunProgramByNameCommand(SdkCommand):
    def __init__(self, program_name: str, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None, enable_feedback: bool = False):
        super().__init__(
            send_command,
            "play_program_name",
            {"name": program_name},
            timeout_seconds,
            throw_error,
            message_bus,
            enable_feedback
        )


class RunPythonProgramCommand(SdkCommand):
    def __init__(self, python_code: str, send_command: Callable[[str, dict], None], env_name: str = "", python_version: str = "3.12", requirements: Optional[List[str]] = None, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None, enable_feedback: bool = False):
        if requirements is None:
            requirements = []
        super().__init__(
            send_command,
            "execute_python_code",
            {
                "env_name": env_name,
                "python_version": python_version,
                "code": python_code,
                "requirements": requirements
            },
            timeout_seconds,
            throw_error,
            message_bus,
            enable_feedback
        )

        data = {
            'env_name': env_name,
            'python_version': python_version,
            'code': python_code,
            'requirements': requirements,
            'velocity_factor': 0.1,
            'acceleration_factor': 0.1
        }
        super().__init__(send_command, 'run_python_program', data, timeout_seconds, throw_error)

    def get_topic(self) -> str:
        return 'manipulator/program/run/python'

@dataclass
class StopMovementCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super().__init__(
            send_command,
            "stop_moving",
            'None',
            timeout_seconds,
            throw_error,
            message_bus
        )


class SetZeroZCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super().__init__(
            send_command,
            "set_zero",
            {"tf_name": "tool1"},
            timeout_seconds,
            throw_error,
            message_bus
        )

    def get_topic(self) -> str:
        return 'manipulator/set_zero_tool'


class WriteAnalogOutputCommand(SdkCommand):
    def __init__(self, channel: int, value: float, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super().__init__(
            send_command,
            "write_analog_output",
            {
                "channel": channel,
                "value": value
            },
            timeout_seconds,
            throw_error,
            message_bus
        )

class WriteDigitalOutputCommand(SdkCommand):
    def __init__(self, channel: int, value: bool, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        super().__init__(
            send_command,
            "write_digital_output",
            {
                "channel": channel,
                "value": value
            },
            timeout_seconds,
            throw_error,
            message_bus
        )


class GetGpio(SdkCommand):
    def __init__(self,
                 send_command: Callable[[str, dict], None],
                 name: str,
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            'get_gpio',
            {'name': name},
            timeout_seconds,
            throw_error,
            message_bus,
        )


class GetI2C(SdkCommand):
    def __init__(self,
                 send_command: Callable[[str, dict], None],
                 name: str,
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            'get_i2c',
            {'name': name},
            timeout_seconds,
            throw_error,
            message_bus,
        )


@dataclass
class WriteGPIO(SdkCommand):
    name: str
    value: int
    send_command: Callable[[str, dict], None]
    timeout_seconds: float = 60.0
    throw_error: bool = True
    message_bus=None

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError('name должен иметь тип str')

        if not isinstance(self.value, int):
            raise TypeError('value должен иметь тип int')

        data: dict[str, Any] = {
            'name': self.name,
            'value': self.value
        }

        super().__init__(self.send_command, 'set_gpio', data, self.timeout_seconds, self.throw_error, self.message_bus)


@dataclass
class WriteI2C(SdkCommand):
    name: str
    value: int
    send_command: Callable[[str, dict], None]
    timeout_seconds: float = 60.0
    throw_error: bool = True
    message_bus=None

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError('name должен иметь тип str')

        if not isinstance(self.value, int):
            raise TypeError('value должен иметь тип int')

        data: dict[str, Any] = {
            'name': self.name,
            'value': self.value
        }

        super().__init__(self.send_command, 'set_i2c', data, self.timeout_seconds, self.throw_error, self.message_bus)


class RunProgramJsonParams(CommandParams):
    program_name: str
    env_name: str = ""
    python_version: str = "3.12"


@dataclass
class JointLimit:
    name: str
    velocity: Union[int, float]
    acceleration: Union[int, float]


@dataclass
class SetJointLimits(SdkCommand):
    limits: list[JointLimit]
    send_command: Callable[[str, dict], None]
    timeout_seconds: float = 60.0
    throw_error: bool = True

    def __post_init__(self):
        data: dict[str, dict[str, Union[int, float]]] = {}
        for limit in self.limits:
            data[limit.name] = {'velocity': limit.velocity, 'acceleration': limit.acceleration}

        super().__init__(self.send_command, 'set_joint_limits', data, self.timeout_seconds, self.throw_error)


@dataclass
class GetJointLimits(SdkCommand):
    send_command: Callable[[str, dict], None]
    timeout_seconds: float = 60.0
    throw_error: bool = True

    def __post_init__(self):
        data = 'None'
        super().__init__(self.send_command, 'get_joint_limits', data, self.timeout_seconds, self.throw_error)
