from abc import abstractmethod
from typing import Callable, Any, Dict
import json
from sdk.commands.abstracts.async_operation import AsyncOperation
from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC, COMMAND_FEEDBACK_TOPIC

_global_command_counter = 0

def get_next_command_id():
    """Получить следующий уникальный ID команды"""
    global _global_command_counter
    _global_command_counter += 1
    return _global_command_counter

class NoWaitCommand:
    """Команда без ожидания ответа - отправляет и забывает"""
    
    def __init__(
        self,
        send_command: Callable[[str, dict], None],
        command_name: str,
        command_data: Any,
        message_bus=None,
    ):
        # Генерируем уникальный ID и сохраняем данные
        self.command_id = get_next_command_id()
        self.command_name = command_name
        self.command_data = command_data
        self.send_command = send_command
        # Ссылка на message_bus (нужна, чтобы сразу удалить себя из active_commands)
        self.message_bus = message_bus

    def make_command_action(self) -> None:
        """Отправляет команду без ожидания ответа"""
        command = {
            "action": "execute",
            "id": self.command_id,
            "command": self.command_name,
            "data": self.command_data
        }
        
        print(f"[NoWaitCommand] Отправляем команду {self.command_name} ID={self.command_id}")
        print(f"[NoWaitCommand] Данные команды: {self.command_data}")
        self.send_command("/command", command)
        print(f"[NoWaitCommand] Команда {self.command_name} ID={self.command_id} отправлена")

        # Если мы были зарегистрированы в active_commands, удаляем себя сразу – ответа не будет
        if self.message_bus and hasattr(self.message_bus, '_manipulator_ref'):
            manipulator = self.message_bus._manipulator_ref
            if manipulator and hasattr(manipulator, 'active_commands'):
                manipulator.active_commands.pop(self.command_id, None)
                print(
                    f"[NoWaitCommand] {self.command_name} ID={self.command_id} удалён из active_commands (NoWait)"
                )

    def process_message(self, topic: str, message: str) -> None:
        """Заглушка для совместимости с active_commands - NoWaitCommand не обрабатывает ответы"""
        pass

class SdkCommand(AsyncOperation):
    
    def __init__(self, send_command: Callable[[str, dict], None], command_name: str, command_data: Any, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None, feedback_converter: bool = False):
        super().__init__(send_command, timeout_seconds, throw_error, feedback_converter)
        
        self.command_id = get_next_command_id()
        
        self.command_name = command_name
        self.command_data = command_data
        self.message_bus = message_bus
        self.feedback_converter = feedback_converter
        self._command_sent = False

    def make_command_action(self) -> None:
        command = {
            "action": "execute",
            "id": self.command_id,
            "command": self.command_name,
            "data": self.command_data
        }
        
        self.send_command("/command", command)

    def get_payload(self) -> Dict[str, Any]:
        return self.command_data
    
    def _cleanup_from_active_commands(self) -> None:
        """Удаляет команду из active_commands манипулятора"""
        if self.message_bus and hasattr(self.message_bus, '_manipulator_ref'):
            try:
                manipulator = self.message_bus._manipulator_ref
                if hasattr(manipulator, 'active_commands') and self.command_id in manipulator.active_commands:
                    del manipulator.active_commands[self.command_id]
                    print(f"[{self.__class__.__name__}] Команда ID={self.command_id} удалена из active_commands")
            except Exception as e:
                print(f"[{self.__class__.__name__}] Ошибка при удалении команды из active_commands: {e}")

    def process_result_message(self, topic: str, message: str) -> None:
        try:
            if isinstance(message, str):
                result_data = json.loads(message)
            else:
                result_data = message
            
            if result_data.get("id") == self.command_id:
                print(f"[{self.__class__.__name__}] Получен ответ для команды {self.command_name} ID={self.command_id}")
                print(f"[{self.__class__.__name__}] Данные ответа: {result_data}")
                
                # Проверяем наличие поля error - если его нет, то команда выполнена успешно
                # независимо от значения result (может быть false для команд типа выключения)
                if "error" not in result_data:
                    print(f"[{self.__class__.__name__}] Команда {self.command_name} выполнена успешно")
                    self.promise.resolve(result_data)
                else:
                    error_msg = result_data.get("error", "Неизвестная ошибка")
                    print(f"[{self.__class__.__name__}] Команда {self.command_name} завершилась с ошибкой: {error_msg}")
                    self.promise.reject(f"Команда {self.command_name} завершилась с ошибкой: {error_msg}")
                self._cleanup_from_active_commands()
            else:
                print(f"[{self.__class__.__name__}] Получен ответ для другой команды: ожидался ID={self.command_id}, получен ID={result_data.get('id')}")
                
        except Exception as e:
            print(f"[{self.__class__.__name__}] Ошибка обработки результата: {str(e)}")
            print(f"[{self.__class__.__name__}] Сырое сообщение: {message}")
            self.promise.reject(f"Ошибка обработки результата: {str(e)}")

    def process_message(self, topic: str, message: str) -> None:
        if not self.promise.is_active:
            return
            
        if self.feedback_converter and topic == COMMAND_FEEDBACK_TOPIC:
            if self.promise and self.promise.is_active:
                self.promise._emit_feedback(self.command_data)
            return
            
        if topic == "/command" and not self._command_sent:
            try:
                data = json.loads(message)
                if (data.get("id") == self.command_id and 
                    data.get("command") == self.command_name):
                    print(f"[{self.__class__.__name__}] Команда отправлена успешно, ID: {self.command_id}")
                    self._command_sent = True
            except json.JSONDecodeError:
                pass
            
        if topic.endswith("/command_result"):
            self.process_result_message(topic, message)

    def result(self):
        res = super().result()
        # if self.message_bus is not None:
        #     try:
        #         from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC
        #         self.message_bus.unsubscribe(COMMAND_TOPIC)
        #         self.message_bus.unsubscribe(COMMAND_RESULT_TOPIC)
        #     except Exception:
        #         pass
        return res
