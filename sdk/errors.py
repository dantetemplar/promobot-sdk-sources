"""Общая иерархия исключений SDK."""

class SdkError(Exception):
    """Базовый класс всех ошибок SDK."""

class CommandError(SdkError):
    """Ошибка выполнения команды."""

class CommandTimeout(SdkError):
    """Таймаут ожидания результата команды/Promise."""

class ConnectionError(SdkError):
    """Проблемы с подключением или публикацией сообщений.""" 