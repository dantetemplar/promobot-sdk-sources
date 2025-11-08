import json
from typing import Optional, Callable, Any
import asyncio
import paho.mqtt.client as mqtt
import time

from sdk.promise import Promise
from sdk.errors import ConnectionError, CommandTimeout
from sdk.utils.message_bus import MessageBus

class ManipulatorConnection(MessageBus):
    connect_future = None
    message_processor: Optional[Callable[[str, str], None]] = None

    def __init__(self, host: str, client_id: str, login: str, password: str, message_processor: Callable[[str, str], None]):
        super().__init__()
        self.host = host
        self.login = login
        self.password = password
        self.client_id = client_id
        self.message_processor = message_processor
        self._manipulator_ref = None
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop()

        self.mqtt_client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def connect(self, **kwargs) -> None:
        self.connect_future = Promise()

        self.mqtt_client.username_pw_set(self.login, self.password)
        self.mqtt_client.connect(self.host, 1883, 60)
        self.mqtt_client.loop_start()

        try:
            self.connect_future.result()
        except CommandTimeout:
            self.mqtt_client.loop_stop()
            raise ConnectionError("Таймаут подключения к MQTT брокеру")

        if not self._connected:
            self.mqtt_client.loop_stop()
            raise ConnectionError("Не удалось подключиться к MQTT брокеру")

    async def connect_async(self) -> None:
        self.connect_future = Promise()
        self.mqtt_client.username_pw_set(self.login, self.password)
        self.mqtt_client.connect(self.host, 1883, 60)
        self.mqtt_client.loop_start()

        try:
            await self.connect_future.async_result()
        except CommandTimeout:
            self.mqtt_client.loop_stop()
            raise ConnectionError("Таймаут подключения к MQTT брокеру")

        if not self._connected:
            self.mqtt_client.loop_stop()
            raise ConnectionError("Не удалось подключиться к MQTT брокеру")

    def disconnect(self) -> None:
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()
        self._connected = False

    def subscribe(self, topic: str) -> None:
        self.mqtt_client.subscribe(topic)

    def unsubscribe(self, topic: str) -> None:
        self.mqtt_client.unsubscribe(topic)

    def publish(self, topic: str, message: Any) -> None:
        self.send_message(topic, message)

    def send_message(self, topic: str, data: Any) -> None:
        payload = data if isinstance(data, str) else json.dumps(data)
        print(f"[MQTT_SEND] Отправляем в топик '{topic}': {payload}")
        result = self.mqtt_client.publish(topic, payload)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise ConnectionError(f"Ошибка отправки сообщения в топик {topic}: код {result.rc}")
        print(f"[MQTT_SEND] Сообщение отправлено успешно (rc={result.rc})")

    async def send_message_async(self, topic: str, data: Any) -> None:
        # Для потоковых сообщений не ждем подтверждения, просто отправляем и возвращаемся
        if topic == "/stream":
            if isinstance(data, str):
                self.mqtt_client.publish(topic, data)
            else:
                self.mqtt_client.publish(topic, json.dumps(data))
            return
        
        # Для других сообщений используем механизм ожидания с таймаутом
        future = asyncio.Future()
        
        def on_publish(client, userdata, mid):
            if not future.done():
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = self._loop
                loop.call_soon_threadsafe(lambda: future.set_result(True))
        
        # Сохраняем предыдущий обработчик для восстановления позже
        previous_on_publish = self.mqtt_client.on_publish
        
        try:
            # Устанавливаем обработчик
            self.mqtt_client.on_publish = on_publish
            
            # Публикуем сообщение
            if isinstance(data, str):
                self.mqtt_client.publish(topic, data)
            else:
                self.mqtt_client.publish(topic, json.dumps(data))
            
            # Ждем завершения публикации с таймаутом и обработкой исключений
            try:
                await asyncio.wait_for(future, 5.0)
            except asyncio.TimeoutError:
                # Если таймаут произошел, просто продолжаем выполнение
                # В большинстве случаев сообщение все равно будет доставлено
                pass
        finally:
            # Восстанавливаем предыдущий обработчик
            self.mqtt_client.on_publish = previous_on_publish

    def on_connect(self, client, userdata, flags, reason_code, properties=None) -> None:
        if isinstance(reason_code, int):
            rc = reason_code
        else:
            rc = int(reason_code) if hasattr(reason_code, '__int__') else 0
        
        if rc == 0:
            self._connected = True
            self.connect_future.resolve(True)
        else:
            self.connect_future.reject(ConnectionError(f"Ошибка подключения к MQTT брокеру (rc={rc})"))

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
        decoded_payload = msg.payload.decode("utf-8")
        if msg.topic == "/command_result":
            print(f"[MQTT] Ответ: {decoded_payload}")
        
        if self.message_processor is not None:
            self.message_processor(msg.topic, decoded_payload)
        else:
            print(f"[MQTT] message_processor не установлен!")