"""
Константы для топиков команд
"""
from enum import Enum, auto

class MessageType(Enum):
    """Типы сообщений"""
    EXECUTE = auto()  # Команды выполнения
    MANAGE = auto()   # Команды управления
    STREAM = auto()   # Команды стриминга
    STATUS = auto()   # Статусные сообщения

# Базовые топики
COMMAND_TOPIC = "/command"
COMMAND_RESULT_TOPIC  ="/command_result"
MANAGEMENT_TOPIC = "/management"
CARTESIAN_COORDINATES_TOPIC = "/coordinates"
JOINT_INFO_TOPIC = "/joint_states"
COMMAND_FEEDBACK_TOPIC = '/feedback'
MGBOT_TOPIC = '/mgbot_info'
PIXY_CAM_COORDINATES_TOPIC = '/pixy_coordinates'

# Маппинг типов сообщений на топики
MESSAGE_TYPE_TO_TOPIC = {
    MessageType.EXECUTE: COMMAND_TOPIC,
    MessageType.MANAGE: MANAGEMENT_TOPIC,
    MessageType.STREAM: COMMAND_TOPIC,
    MessageType.STATUS: COMMAND_RESULT_TOPIC
}

# Маппинг типов сообщений на топики результатов
MESSAGE_TYPE_TO_RESULT_TOPIC = {
    MessageType.EXECUTE: COMMAND_RESULT_TOPIC,
    MessageType.MANAGE: MANAGEMENT_TOPIC,
    MessageType.STREAM: COMMAND_RESULT_TOPIC,
    MessageType.STATUS: COMMAND_RESULT_TOPIC
}
