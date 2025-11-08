from typing import Any, Dict

from .base import Attachment
from sdk.commands.vacuum_control_command import VacuumControlCommand


class VacuumAttachment(Attachment):
    """Насадка-вакуум для MEdu.
    Отправляет команды напрямую через message_bus
    """

    def __init__(self, manipulator, name: str = "vacuum", rotation: int = 0):
        super().__init__(name)
        self.rotation = rotation
        self._status = "idle"
        
        # Сохраняем ссылку на манипулятор и регистрируемся
        self._manipulator = manipulator
        manipulator.register_attachment(self)

    # -------------------------------------------------
    def activate(self, rotation: int = None, timeout_seconds: float = 60.0, throw_error: bool = True, **kwargs) -> None:
        """Включить вакуум."""
        rotation = rotation if rotation is not None else self.rotation
        command = VacuumControlCommand(
            self.manipulator.message_bus.publish,
            rotation,
            True,  # power_supply=True
            timeout_seconds,
            throw_error,
            message_bus=self.manipulator.message_bus
        )
        # Регистрируем команду в active_commands для отслеживания ответа
        self.manipulator.active_commands[command.command_id] = command
        command.make_command_action()
        try:
            command.result()
        finally:
            if command.command_id in self.manipulator.active_commands:
                del self.manipulator.active_commands[command.command_id]
        self._status = "active"

    def deactivate(self, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """Выключить вакуум."""
        command = VacuumControlCommand(
            self.manipulator.message_bus.publish,
            self.rotation,
            False,  # power_supply=False
            timeout_seconds,
            throw_error,
            message_bus=self.manipulator.message_bus
        )
        # Регистрируем команду в active_commands для отслеживания ответа
        self.manipulator.active_commands[command.command_id] = command
        command.make_command_action()
        try:
            command.result()
        finally:
            if command.command_id in self.manipulator.active_commands:
                del self.manipulator.active_commands[command.command_id]
        self._status = "idle"

    def get_status(self) -> str:
        return self._status