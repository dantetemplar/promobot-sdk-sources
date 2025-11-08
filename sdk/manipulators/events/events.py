from typing import Callable, Dict, Any, Optional
from sdk.utils.constants import (
    COMMAND_TOPIC,
    COMMAND_RESULT_TOPIC,
    MANAGEMENT_TOPIC,
    CARTESIAN_COORDINATES_TOPIC,
    JOINT_INFO_TOPIC
)


class EventMixin:

    def __init__(self):
        # Обработчики событий
        self._on_message: Optional[Callable] = None  # общий для всех топиков
        self._on_command: Optional[Callable] = None
        self._on_command_result: Optional[Callable] = None
        self._on_management: Optional[Callable] = None
        self._on_coordinates: Optional[Callable] = None
        self._on_joint_states: Optional[Callable] = None
        
        # _topic_handlers убран за ненадобностью; обработка выполняется через on_message
    
    def _call_handler(self, handler: Optional[Callable], message: Any) -> None:
        """Безопасный вызов обработчика"""
        if handler:
            try:
                handler(message)
            except Exception as e:
                print(f"Ошибка в обработчике события: {e}")
    
    # Properties для удобного присваивания обработчиков
    @property
    def on_command(self) -> Optional[Callable]:
        return self._on_command
    
    @on_command.setter
    def on_command(self, handler: Callable) -> None:
        self._on_command = handler
        if hasattr(self, "message_bus"):
            self.message_bus.on_message(COMMAND_TOPIC, handler)
    
    @property
    def on_command_result(self) -> Optional[Callable]:
        return self._on_command_result
    
    @on_command_result.setter
    def on_command_result(self, handler: Callable) -> None:
        self._on_command_result = handler
        if hasattr(self, "message_bus"):
            self.message_bus.on_message(COMMAND_RESULT_TOPIC, handler)
    
    @property
    def on_management(self) -> Optional[Callable]:
        return self._on_management
    
    @on_management.setter
    def on_management(self, handler: Callable) -> None:
        self._on_management = handler
        if hasattr(self, "message_bus"):
            self.message_bus.on_message(MANAGEMENT_TOPIC, handler)
    
    @property
    def on_coordinates(self) -> Optional[Callable]:
        return self._on_coordinates
    
    @on_coordinates.setter
    def on_coordinates(self, handler: Callable) -> None:
        self._on_coordinates = handler
        if hasattr(self, "message_bus"):
            self.message_bus.on_message(CARTESIAN_COORDINATES_TOPIC, handler)
    
    @property
    def on_joint_states(self) -> Optional[Callable]:
        return self._on_joint_states
    
    @on_joint_states.setter
    def on_joint_states(self, handler: Callable) -> None:
        self._on_joint_states = handler
        if hasattr(self, "message_bus"):
            self.message_bus.on_message(JOINT_INFO_TOPIC, handler)

    # Универсальный обработчик всех сообщений
    @property
    def on_message(self) -> Optional[Callable]:
        return self._on_message

    @on_message.setter
    def on_message(self, handler: Callable[[str, Any], None]) -> None:  # type: ignore
        self._on_message = handler
        if hasattr(self, "message_bus") and callable(handler):
            # регистрируем обработчик, который передаёт topic + payload
            def _wrapper(msg_topic: str, payload: Any):
                try:
                    handler(msg_topic, payload)
                except Exception as e:
                    print(f"Ошибка в on_message: {e}")

            self.message_bus.on_message("#", _wrapper)  # подписываемся на все 