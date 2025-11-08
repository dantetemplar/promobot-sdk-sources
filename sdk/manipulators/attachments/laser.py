from typing import Any, Dict

from .base import Attachment
from sdk.commands.manipulator_commands import WriteDigitalOutputCommand


class LaserAttachment(Attachment):
    """Насадка-лазер для MEdu.
    Отправляет команды напрямую через message_bus
    """

    def __init__(self, manipulator, channel: int, name: str = "laser"):
        super().__init__(name)
        self.channel = channel
        self._status = "off"
        
        self._manipulator = manipulator
        manipulator.register_attachment(self)

    # -------------------------------------------------
    def activate(self, timeout_seconds: float = 60.0, throw_error: bool = True, **kwargs) -> None:
        """Включить лазер."""
        command = WriteDigitalOutputCommand(
            self.channel,
            True,
            self.manipulator.message_bus.publish,
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
        self._status = "on"

    def deactivate(self, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """Выключить лазер."""
        command = WriteDigitalOutputCommand(
            self.channel,
            False,
            self.manipulator.message_bus.publish,
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
        self._status = "off"

    def get_status(self) -> str:
        return self._status