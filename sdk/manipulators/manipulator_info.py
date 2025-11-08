from typing import Optional, Dict, Any
import json
from sdk.promise import Promise
from sdk.utils.message_bus import MessageBus
from sdk.manipulators.manipulator_connection import ManipulatorConnection
from sdk.commands.abstracts.sdk_command import SdkCommand

class ManipulatorInfo:
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self._manipulator_ref = None  # Ссылка на родительский манипулятор для доступа к его методам
        self._info_promise: Optional[Promise] = None
        self._hardware_state_promise: Optional[Promise] = None
        self._joint_states_promise: Optional[Promise] = None
        self._coordinates_promise: Optional[Promise] = None
        self._coordinate_limits_promise: Optional[Promise] = None
        self._gamepad_info_promise: Optional[Promise] = None
        self._gpio_states_promise: Optional[Promise] = None
        self._command_result_states_promise: Optional[Promise] = None
        self._i2c_states_promise: Optional[Promise] = None

        self._last_info: Optional[str] = None
        self._last_hardware_state: Optional[str] = None
        self._last_joint_states: Optional[str] = None
        self._last_coordinates: Optional[str] = None
        self._last_coordinate_limits: Optional[str] = None
        self._last_gamepad_info: Optional[str] = None
        self._last_gpio_states: Optional[str] = None
        self._last_command_result_states: Optional[str] = None
        self._last_i2c_states: Optional[str] = None

    def process_message(self, topic: str, payload: str) -> None:
        topic_mapping = {
            "/manipulator_info": ("_last_info", "_info_promise"),
            "/hardware_state": ("_last_hardware_state", "_hardware_state_promise"),
            "/joint_states": ("_last_joint_states", "_joint_states_promise"),
            "/coordinates": ("_last_coordinates", "_coordinates_promise"),
            "/coordinate_limits": ("_last_coordinate_limits", "_coordinate_limits_promise"),
            "/gamepad_info": ("_last_gamepad_info", "_gamepad_info_promise"),
            "/gpio_states": ("_last_gpio_states", "_gpio_states_promise"),
            "/i2c_states": ("_last_i2c_states", "_i2c_states_promise"),
            '/command_result': ('_last_command_result_states', '_command_result_states_promise')
        }

        if topic in topic_mapping:
            last_attr, promise_attr = topic_mapping[topic]
            promise = getattr(self, promise_attr)
            # Проверяем, что в атрибуте действительно хранится объект Promise.
            if isinstance(promise, Promise):
                setattr(self, last_attr, payload)
                try:
                    promise.resolve(True)
                except Exception as e:
                    print(f"[ManipulatorInfo] Ошибка при promise.resolve: {e}")
            elif promise is not None:
                print(f"[ManipulatorInfo] Предупреждение: {promise_attr} имеет тип {type(promise).__name__}, ожидается Promise")

    async def _safe_get_data_async(self, topic: str, promise: Promise, last_data: Optional[str], timeout_seconds: float) -> Dict[str, Any]:
        """Безопасное получение данных с обработкой исключений (асинхронная версия)"""
        try:
            if not hasattr(self.message_bus, "subscribe"):
                raise Exception("[ManipulatorInfo] Атрибут message_bus повреждён: отсутствует метод subscribe")
            self.message_bus.subscribe(topic)
            await promise.async_result()
            return json.loads(last_data) if last_data else {}
        except Exception as e:
            raise Exception(f"Ошибка при получении данных из топика {topic}: {str(e)}")
        finally:
            try:
                self.message_bus.unsubscribe(topic)
            except:
                pass

    def _safe_get_data(self, topic: str, promise: Promise, last_data: Optional[str], timeout_seconds: float) -> Dict[str, Any]:
        """Безопасное получение данных с обработкой исключений"""
        try:
            if not hasattr(self.message_bus, "subscribe"):
                raise Exception("[ManipulatorInfo] Атрибут message_bus повреждён: отсутствует метод subscribe")
            self.message_bus.subscribe(topic)
            promise.result()
            return json.loads(last_data) if last_data else {}
        except Exception as e:
            # Для топиков, которые могут быть недоступны, возвращаем информацию об ошибке вместо исключения
            if topic in ["/hardware_state", "/joint_states"]:
                print(f"[ManipulatorInfo] Топик {topic} недоступен: {str(e)}")
                return {"error": f"topic_{topic.replace('/', '').replace('_', '')}_unavailable", "message": str(e)}
            else:
                raise Exception(f"Ошибка при получении данных из топика {topic}: {str(e)}")
        finally:
            try:
                self.message_bus.unsubscribe(topic)
            except:
                pass

    def get_result_command(self, command: Optional[SdkCommand],  timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить ответ от команды"""
        self._command_result_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            command.result()
            return self._safe_get_data('/command_result', self._command_result_states_promise, self._last_command_result_states, timeout_seconds)
        finally:
            self._command_result_states_promise = None
            
    async def get_result_command_async(self, command: Optional[SdkCommand], timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить ответ от команды (асинхронная версия)"""
        self._command_result_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            await command.async_result()
            return await self._safe_get_data_async('/command_result', self._command_result_states_promise, self._last_command_result_states, timeout_seconds)
        finally:
            self._command_result_states_promise = None
    
    def get_manipulator_info(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить информацию о манипуляторе"""
        self._info_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/manipulator_info", self._info_promise, self._last_info, timeout_seconds)
        finally:
            self._info_promise = None

    async def get_manipulator_info_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить информацию о манипуляторе (асинхронная версия)"""
        self._info_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/manipulator_info", self._info_promise, self._last_info, timeout_seconds)
        finally:
            self._info_promise = None

    def get_hardware_state(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние аппаратной части"""
        self._hardware_state_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/hardware_state", self._hardware_state_promise, self._last_hardware_state, timeout_seconds)
        finally:
            self._hardware_state_promise = None

    async def get_hardware_state_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние аппаратной части (асинхронная версия)"""
        self._hardware_state_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/hardware_state", self._hardware_state_promise, self._last_hardware_state, timeout_seconds)
        finally:
            self._hardware_state_promise = None

    def get_joint_states(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние узлов"""
        # Используем существующий рабочий механизм из манипулятора
        if self._manipulator_ref is not None:
            try:
                joint_state_str = self._manipulator_ref.get_joint_state(timeout_seconds)
                return json.loads(joint_state_str) if joint_state_str else {}
            except Exception as e:
                raise Exception(f"Ошибка при получении состояния суставов: {str(e)}")
        else:
            # Fallback к старому методу, если нет ссылки на манипулятор
            self._joint_states_promise = Promise(timeout_seconds=timeout_seconds)
            try:
                return self._safe_get_data("/joint_states", self._joint_states_promise, self._last_joint_states, timeout_seconds)
            finally:
                self._joint_states_promise = None

    async def get_joint_states_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние узлов (асинхронная версия)"""
        self._joint_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/joint_states", self._joint_states_promise, self._last_joint_states, timeout_seconds)
        finally:
            self._joint_states_promise = None

    def get_coordinates(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить текущие координаты"""
        # Используем существующий рабочий механизм из манипулятора
        if self._manipulator_ref is not None:
            try:
                coordinates_str = self._manipulator_ref.get_cartesian_coordinates(timeout_seconds)
                return json.loads(coordinates_str) if coordinates_str else {}
            except Exception as e:
                raise Exception(f"Ошибка при получении координат: {str(e)}")
        else:
            # Fallback к старому методу, если нет ссылки на манипулятор
            self._coordinates_promise = Promise(timeout_seconds=timeout_seconds)
            try:
                return self._safe_get_data("/coordinates", self._coordinates_promise, self._last_coordinates, timeout_seconds)
            finally:
                self._coordinates_promise = None

    async def get_coordinates_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить текущие координаты (асинхронная версия)"""
        self._coordinates_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/coordinates", self._coordinates_promise, self._last_coordinates, timeout_seconds)
        finally:
            self._coordinates_promise = None

    def get_coordinate_limits(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить пределы в координатах"""
        self._coordinate_limits_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/coordinate_limits", self._coordinate_limits_promise, self._last_coordinate_limits, timeout_seconds)
        finally:
            self._coordinate_limits_promise = None

    async def get_coordinate_limits_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить пределы в координатах (асинхронная версия)"""
        self._coordinate_limits_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/coordinate_limits", self._coordinate_limits_promise, self._last_coordinate_limits, timeout_seconds)
        finally:
            self._coordinate_limits_promise = None

    def get_gamepad_info(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить информацию о геймпаде"""
        self._gamepad_info_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/gamepad_info", self._gamepad_info_promise, self._last_gamepad_info, timeout_seconds)
        finally:
            self._gamepad_info_promise = None

    async def get_gamepad_info_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить информацию о геймпаде (асинхронная версия)"""
        self._gamepad_info_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/gamepad_info", self._gamepad_info_promise, self._last_gamepad_info, timeout_seconds)
        finally:
            self._gamepad_info_promise = None

    def get_gpio_states(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние GPIO"""
        self._gpio_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/gpio_states", self._gpio_states_promise, self._last_gpio_states, timeout_seconds)
        finally:
            self._gpio_states_promise = None

    async def get_gpio_states_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние GPIO (асинхронная версия)"""
        self._gpio_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/gpio_states", self._gpio_states_promise, self._last_gpio_states, timeout_seconds)
        finally:
            self._gpio_states_promise = None

    def get_i2c_states(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние I2C устройств"""
        self._i2c_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return self._safe_get_data("/i2c_states", self._i2c_states_promise, self._last_i2c_states, timeout_seconds)
        finally:
            self._i2c_states_promise = None

    async def get_i2c_states_async(self, timeout_seconds: float = 60.0) -> Dict[str, Any]:
        """Получить состояние I2C устройств (асинхронная версия)"""
        self._i2c_states_promise = Promise(timeout_seconds=timeout_seconds)
        try:
            return await self._safe_get_data_async("/i2c_states", self._i2c_states_promise, self._last_i2c_states, timeout_seconds)
        finally:
            self._i2c_states_promise = None 