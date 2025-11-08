from enum import Enum


class ManipulatorState(Enum):
    """
    Перечисление состояний манипулятора.
    """
    IDLE = 0
    AUTO = 1
    MANUAL = 2
    CALIBRATION = 3
    EMERGENCY_STOP = 4
    TEACHING = 5
    ERROR = 6
    ACTIVE_REAL = 7


class ServoControlType(Enum):
    """
    Перечисление типов управления сервоприводом.
    """
    JOINT_JOG = 0
    TWIST = 1
    POSE = 2
