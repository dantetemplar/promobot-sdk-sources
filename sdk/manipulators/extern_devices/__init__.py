"""
Package для внешних устройств манипулятора (pixy, mgbot и т.д.).
Экспортирует подмодули и часто используемые классы для удобного импорта:
from sdk.manipulators.extern_devices import pixy_cam, mgbot
from sdk.manipulators.extern_devices import PixyCamUartModule
"""


from . import pixy_cam
from . import mgbot


try:
    from .pixy_cam import PixyCamModuleBase, PixyCamUartModule, PixyCamUsbModule
except Exception:
    PixyCamModuleBase = None
    PixyCamUartModule = None
    PixyCamUsbModule = None


try:
    from .mgbot import MGbotConveyer
except Exception:
    MGbotConveyer = None


__all__ = [
    "pixy_cam",
    "mgbot",
    "PixyCamModuleBase",
    "PixyCamUartModule",
    "PixyCamUsbModule",
    "MGbotConveyer",
]