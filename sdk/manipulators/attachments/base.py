from abc import ABC, abstractmethod
from typing import Dict
from .host import AttachmentHost
# Добавляем недостающий импорт Any
from typing import Any

class Attachment(ABC):
    """Базовый класс насадки."""

    def __init__(self, name: str):
        self.name = name
        self._manipulator = None  # будет установлено при attach

    # -------------------------------------------------
    # Жизненный цикл
    # -------------------------------------------------
    def attach(self, manipulator: AttachmentHost) -> None:
        """Привязать к манипулятору."""
        self._manipulator = manipulator
        self.on_attached()

    def detach(self) -> None:
        """Отвязать от манипулятора."""
        try:
            self.on_detached()
        finally:
            self._manipulator = None

    # -------------------------------------------------
    # Хуки
    # -------------------------------------------------
    def on_attached(self) -> None:  # noqa: D401
        pass

    def on_detached(self) -> None:  # noqa: D401
        pass

    # -------------------------------------------------
    # Абстрактное API
    # -------------------------------------------------
    @abstractmethod
    def activate(self, timeout_seconds: float = 60.0, throw_error: bool = True, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def deactivate(self, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError

    # -------------------------------------------------
    @property
    def manipulator(self) -> AttachmentHost:
        if self._manipulator is None:
            raise RuntimeError("Attachment is not registered")
        return self._manipulator

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name}>" 