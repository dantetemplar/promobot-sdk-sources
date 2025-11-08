"""Событийный API для манипуляторов.

Экспортируются удобные декораторы, назначающие обработчики сообщений на нужные
топики. Предполагается, что используются вместе с экземпляром класса,
наследующего :class:`EventMixin` (например, `Manipulator`).
"""

from functools import wraps
from typing import Callable, Any

from sdk.manipulators.events.events import EventMixin  # noqa: F401 – публичный экспорт
from sdk.utils.constants import (
    COMMAND_TOPIC,
    COMMAND_RESULT_TOPIC,
    MANAGEMENT_TOPIC,
    CARTESIAN_COORDINATES_TOPIC,
    JOINT_INFO_TOPIC,
)

# -------------------------------------------------
# Декораторы
# -------------------------------------------------


def _make_topic_decorator(topic: str):
    """Строит декоратор, который фильтрует входящие сообщения по *topic* через self.on_message."""

    def decorator(func: Callable[[Any], None]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):  # type: ignore[override]
            # Назначаем единый on_message если ещё не назначен
            previous = getattr(self, "on_message", None)

            def _handler(msg_topic: str, payload: Any):
                if msg_topic == topic:
                    func(self, payload)
                if callable(previous):
                    previous(msg_topic, payload)

            if previous is not _handler:
                self.on_message = _handler  # type: ignore[attr-defined]

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


# Создаём конкретные декораторы
on_message = _make_topic_decorator("*")
on_command = _make_topic_decorator(COMMAND_TOPIC)
on_command_result = _make_topic_decorator(COMMAND_RESULT_TOPIC)
on_management = _make_topic_decorator(MANAGEMENT_TOPIC)
on_coordinates = _make_topic_decorator(CARTESIAN_COORDINATES_TOPIC)
on_joint_states = _make_topic_decorator(JOINT_INFO_TOPIC)

# Для совместимости: экспорт «EventHandler» как алиас EventMixin
EventHandler = EventMixin

__all__ = [
    "on_message",
    "on_command",
    "on_command_result",
    "on_management",
    "on_coordinates",
    "on_joint_states",
    "EventHandler",
] 