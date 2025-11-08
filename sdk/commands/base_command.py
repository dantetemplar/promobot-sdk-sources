from pydantic import BaseModel, Field

class CommandParams(BaseModel):
    """Класс параметров команд с валидацией через pydantic.
    Оставлен для обратной совместимости (используется в manipulator_commands)."""
    class Config:
        extra = "forbid"  # Запрещаем лишние поля
        validate_assignment = True