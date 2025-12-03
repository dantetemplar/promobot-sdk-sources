from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass, field
from sdk.commands.data import Point3D
from sdk.commands.abstracts.sdk_command import SdkCommand
from sdk.commands.base_command import CommandParams
from sdk.commands.data import Point3D, JointPositions

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
    def __init__(self, python_code: str, send_command: Callable[[str, dict], None], python_version: str = "3.12", requirements: Optional[List[str]] = None, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None, enable_feedback: bool = False):
        if requirements is None:
            requirements = []
            
        data = {
            'python_version': python_version,
            'code': python_code,
            'requirements': requirements,
        }
        super().__init__(
            send_command,
            "execute_python_code",
            data,
            timeout_seconds,
            throw_error,
            message_bus,
            enable_feedback
        )

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


class TCPDelete(SdkCommand):
    def __init__(self,
                 name: str,
                 send_command: Callable[[str, dict], None],
                 reset_current: bool = True,
                 apply_other: str = "",
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            "tcp_delete",
            {
                "name": name,
                "reset_current": reset_current,
                "apply_other": apply_other
            },
            timeout_seconds,
            throw_error,
            message_bus
        )


class TCPAdd(SdkCommand):
    def __init__(self,
                 name: str,
                 position: Point3D,
                 apply: bool,
                 send_command: Callable[[str, dict], None],
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus=None):
        super().__init__(
            send_command,
            "tcp_add",
            {
                'name': name,
                'pose': position.to_dict(),
                'apply': apply
            },
            timeout_seconds,
            throw_error,
            message_bus
        )


class TCPApply(SdkCommand):
    def __init__(self,
                 name: str,
                 send_command: Callable[[str, dict], None],
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            "tcp_apply",
            {"name": name},
            timeout_seconds,
            throw_error,
            message_bus
        )


class TCPGetCurrent(SdkCommand):
    def __init__(self,
                 send_command: Callable[[str, dict], None],
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            "tcp_get_current",
            "None",
            timeout_seconds,
            throw_error,
            message_bus
        )


class TCPGetList(SdkCommand):
    def __init__(self,
                 send_command: Callable[[str, dict], None],
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            "tcp_get_list",
            "None",
            timeout_seconds,
            throw_error,
            message_bus
        )


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


class GPIOConfigurePin(SdkCommand):
    def __init__(self,
                 send_command: Callable[[str, dict], None],
                 name: str,
                 value: bool,
                 timeout_seconds: float = 60.0,
                 throw_error: bool = True,
                 message_bus = None):
        super().__init__(
            send_command,
            'gpio_pin_configure',
            {
                'name': name,
                "active": value
            },
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


@dataclass
class MoveGroup(SdkCommand):
    send_command: Callable[[str, dict], None]
    points: List[Point3D] = field(default_factory=list)
    positions: List[JointPositions] = field(default_factory=list)
    move_group: str = "main"
    planning_pipeline: str = "pilz_industrial_motion_planner"
    planner_id: str = "PTP"
    max_velocity: float = 0.5
    max_acceleration: float = 0.5
    min_factorial: float = 0.95
    steps: float = 0.05
    count_points: int = 50
    timeout_seconds: float = 60.0
    throw_error: bool = True

    def __post_init__(self):
        data: dict[str, Any] = {
            "points": [point.to_dict() for point in self.points],
            "positions": [jp.to_dict() for jp in self.positions],
            "move_group": self.move_group,
            "planning_pipeline": self.planning_pipeline,
            "planner_id": self.planner_id,
            "max_velocity": self.max_velocity,
            "max_acceleration": self.max_acceleration,
            "min_factorial": self.min_factorial,
            "steps": self.steps,
            "count_points": self.count_points
        }

        super().__init__(
            self.send_command,
            'move_group',
            data,
            self.timeout_seconds,
            self.throw_error
        )
