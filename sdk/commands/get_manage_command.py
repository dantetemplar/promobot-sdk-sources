import json

from sdk.commands.abstracts.sdk_command import SdkCommand
from typing import Callable


class GetManageCommand(SdkCommand):
    def __init__(self, send_command: Callable[[str, dict], None], current_client_id: str, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        self.client_id = current_client_id
        print(f"[GET_MANAGE_CMD] Инициализация с client_id: '{self.client_id}'")
        # Используем SdkCommand с командой управления
        super(GetManageCommand, self).__init__(
            send_command, 
            "get_management", 
            {"get_management": True}, 
            timeout_seconds, 
            throw_error, 
            message_bus
        )
        print(f"[GET_MANAGE_CMD] Инициализирован command_id: {self.command_id}")

    def make_command_action(self) -> None:
        print(f"[GET_MANAGE_CMD] make_command_action() вызван")
        # Отправляем команду с ID для правильной корреляции ответов
        self.send_command("/management", {
            "get_management": True,
            "id": self.command_id
        })
        print(f"[GET_MANAGE_CMD] Команда отправлена в /management с ID: {self.command_id}")

    def process_message(self, topic: str, message: str) -> None:
        # Быстрая проверка перед логированием
        if not self.promise.is_active:
            return
            
        print(f"[GET_MANAGE_CMD] process_message: топик='{topic}', сообщение='{message}'")
        
        # Если promise уже неактивен, не обрабатываем сообщения
        if not self.promise.is_active:
            print(f"[GET_MANAGE_CMD] Promise неактивен, пропускаем обработку сообщения")
            return
        
        # Обрабатываем ответы из /management (основной ответ о получении управления)
        if topic == "/management" and message.__contains__("management_client_id"):
            print(f"[GET_MANAGE_CMD] Обрабатываем ответ управления...")
            get_management_data = json.loads(message)
            management_client_id = get_management_data.get("management_client_id", None)
            print(f"[GET_MANAGE_CMD] management_client_id из ответа: '{management_client_id}' (тип: {type(management_client_id)})")
            print(f"[GET_MANAGE_CMD] self.client_id: '{self.client_id}' (тип: {type(self.client_id)})")
            print(f"[GET_MANAGE_CMD] Сравнение: {management_client_id} == {self.client_id} -> {management_client_id == self.client_id}")
            
            if management_client_id == self.client_id:
                print(f"[GET_MANAGE_CMD] СОВПАДЕНИЕ! Вызываем promise.resolve(True)...")
                self.promise.resolve(True)
                print(f"[GET_MANAGE_CMD] promise.resolve(True) вызван")
                return
            else:
                print(f"[GET_MANAGE_CMD] НЕ СОВПАДАЕТ! Отклоняем promise...")
                print(message)
                self.promise.reject("Управление не предоставлено")
                return
        
        # Также обрабатываем стандартные ответы из /command_result
        if topic == "/command_result":
            print(f"[GET_MANAGE_CMD] Обрабатываем /command_result...")
            try:
                command_data = json.loads(message)
                command_id = command_data.get("id", None)
                result = command_data.get("result", None)
                print(f"[GET_MANAGE_CMD] command_id из /command_result: {command_id}, result: {result}")
                
                # Проверяем, что это ответ на нашу команду
                if command_id == self.command_id and result is not None:
                    print(f"[GET_MANAGE_CMD] /command_result соответствует нашей команде, но ждем ответа в /management")
                    # Команда была выполнена, но ждем ответа в /management
                    # Ничего не делаем, просто принимаем к сведению
                    pass
            except json.JSONDecodeError:
                print(f"[GET_MANAGE_CMD] Ошибка парсинга JSON в /command_result")
                pass
        
        print(f"[GET_MANAGE_CMD] process_message завершен")