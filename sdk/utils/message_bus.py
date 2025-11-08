from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class MessageFormat(Enum):
    """Форматы сообщений"""
    JSON = "json"
    BINARY = "binary"
    TEXT = "text"

@dataclass
class MessageSpec:
    """Спецификация формата сообщения"""
    topic: str
    input_format: MessageFormat
    output_format: MessageFormat
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    description: str = ""


class MessageBus(ABC):
    """Абстрактный базовый класс для работы с шиной данных"""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._message_specs: Dict[str, MessageSpec] = {}
        self._connected = False
        self.command_id = 0

    @property
    def is_connected(self) -> bool:
        return self._connected

    def generate_id(self) -> int:
        self.command_id += 1
        return self.command_id
    @abstractmethod
    def connect(self, **kwargs) -> None:
        """Подключение к шине данных"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Отключение от шины данных"""
        pass

    @abstractmethod
    def publish(self, topic: str, message: Any) -> None:
        """Публикация сообщения в топик"""
        pass

    @abstractmethod
    def subscribe(self, topic: str) -> None:
        """Подписка на топик"""
        pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        """Отписка от топика"""
        pass
        
    def register_message_spec(self, spec: MessageSpec) -> None:
        """Регистрация спецификации формата сообщения"""
        self._message_specs[spec.topic] = spec
        
    def get_message_spec(self, topic: str) -> Optional[MessageSpec]:
        """Получение спецификации формата сообщения"""
        return self._message_specs.get(topic)
        
    def on_message(self, topic: str, handler: Callable) -> None:
        """
        Регистрация обработчика сообщений для топика
        
        Args:
            topic: Название топика
            handler: Функция-обработчик вида handler(message)
        """
        if topic not in self._handlers:
            self._handlers[topic] = []
            self.subscribe(topic)
            
        self._handlers[topic].append(handler)

    def off_message(self, topic: str, handler: Callable) -> None:
        """Удаление обработчика сообщений"""
        if topic in self._handlers and handler in self._handlers[topic]:
            self._handlers[topic].remove(handler)
            
            # Если больше нет обработчиков, отписываемся от топика
            if not self._handlers[topic]:
                self.unsubscribe(topic)
                del self._handlers[topic]
                
    def _process_message(self, topic: str, message: Any) -> None:
        """Обработка полученного сообщения"""
        if topic in self._handlers:
            for handler in self._handlers[topic]:
                try:
                    handler(message)
                except Exception as e:
                    self._handle_error(topic, handler, e)
                    
    def _handle_error(self, topic: str, handler: Callable, error: Exception) -> None:
        """Обработка ошибок в обработчиках"""
        print(f"Ошибка в обработчике для топика {topic}: {error}") 