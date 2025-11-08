"""
Модуль для работы с манипуляторами
"""

from sdk.manipulators.manipulator import Manipulator  # старое имя
from sdk.manipulators.base import BaseManipulator
from sdk.manipulators.medu import MEdu
from sdk.manipulators.m13 import M13
from sdk.manipulators.attachments import (
    Attachment,
    LaserAttachment,
    GripperAttachment,
    VacuumAttachment,
)

__all__ = [
    "Manipulator",
    "BaseManipulator",
    "MEdu",
    "M13",
    "Attachment",
    "LaserAttachment",
    "GripperAttachment",
    "VacuumAttachment",
]