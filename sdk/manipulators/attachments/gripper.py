from typing import Any, Dict

from .base import Attachment
from sdk.commands.gripper_control_command import GripperControlCommand


class GripperAttachment(Attachment):
    """Насадка-гриппер для MEdu.
    Отправляет команды напрямую через message_bus
    """

    def __init__(self, manipulator, name: str = "gripper", rotation_open: int = 0, gripper_open: int = 40):
        super().__init__(name)
        self.rotation_open = rotation_open
        self.gripper_open = gripper_open
        self._status = "idle"

        # Сохраняем ссылку на манипулятор и регистрируемся
        self._manipulator = manipulator
        manipulator.register_attachment(self)

    # -------------------------------------------------
    def activate(self, rotation: int = None, gripper: int = None, timeout_seconds: float = 60.0, throw_error: bool = True, **kwargs) -> None:
        """Закрыть гриппер (зажать предмет)."""
        if rotation == None and gripper == None:
            rotation = self.rotation_open
            gripper = 0
        command = GripperControlCommand(
            self.manipulator.message_bus.publish, 
            rotation,
            gripper,
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
        """Открыть гриппер."""
        command = GripperControlCommand(
            self.manipulator.message_bus.publish,
            self.rotation_open,
            self.gripper_open,
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