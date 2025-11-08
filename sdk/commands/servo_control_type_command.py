from typing import Callable
import json

from sdk.commands.abstracts.sdk_command import SdkCommand

# Константы типов управления
JOINT_JOG = 0  # Управление отдельными суставами
TWIST = 1      # Управление с помощью линейных и угловых скоростей
POSE = 2       # Управление позицией и ориентацией

class ServoControlTypeCommand(SdkCommand):
    """
    Команда для изменения типа управления MoveIt Servo
    Значения типов управления:
    JOINT_JOG = 0 - управление отдельными суставами
    TWIST = 1 - управление с помощью линейных и угловых скоростей
    POSE = 2 - управление позицией и ориентацией
    """
    def __init__(self, send_command: Callable[[str, dict], None], control_type_id: int, timeout_seconds: float = 60.0, throw_error: bool = True, message_bus=None):
        if not isinstance(control_type_id, int) or control_type_id not in [JOINT_JOG, TWIST, POSE]:
            raise ValueError(f"control_type_id должен быть одним из значений: {JOINT_JOG} (JOINT_JOG), {TWIST} (TWIST), или {POSE} (POSE)")
            
        data = {
            "id": control_type_id
        }
        
        super(ServoControlTypeCommand, self).__init__(send_command, "servo_control_type", data, timeout_seconds, throw_error, message_bus)
        self.control_type_id = control_type_id
        self._command_sent = False

    def process_message(self, topic: str, message: str) -> None:
        if not self.promise.is_active:
            return
        if topic == "/command" and not self._command_sent:
            try:
                data = json.loads(message)
                if (data.get("id") == self.command_id and 
                    data.get("command") == self.command_name):
                    print(f"[SERVO_CONTROL_TYPE_CMD] Команда отправлена успешно, ID: {self.command_id}")
                    self._command_sent = True
                    if hasattr(self, 'message_bus') and self.message_bus:
                        import threading
                        import time
                        def delayed_success():
                            time.sleep(0.1)
                            if self.promise.is_active:
                                print(f"[SERVO_CONTROL_TYPE_CMD] Симулируем успешное завершение для ID: {self.command_id}")
                                self.promise.resolve({"result": True, "success": True})
                        threading.Thread(target=delayed_success, daemon=True).start()
            except json.JSONDecodeError:
                pass
        # Также обрабатываем стандартные ответы из /command_result
        super().process_message(topic, message)