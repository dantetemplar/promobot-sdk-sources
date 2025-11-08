"""Насадки (attachments) для манипуляторов

Пользователь может регистрировать насадки в объекте Manipulator при помощи
`manipulator.register_attachment(instance)`.
"""

from .base import Attachment
from .laser import LaserAttachment
from .gripper import GripperAttachment
from .vacuum import VacuumAttachment

__all__ = [
    "Attachment",
    "LaserAttachment",
    "GripperAttachment",
    "VacuumAttachment",
] 