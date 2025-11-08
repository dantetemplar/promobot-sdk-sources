# ПРОМОБОТ Python SDK - Полная документация для пользователей

## Содержание

1. [Установка и быстрый старт](#установка-и-быстрый-старт)
2. [Подключение к манипулятору](#подключение-к-манипулятору)
3. [Управление движением](#управление-движением)
4. [Работа с насадками](#работа-с-насадками)
5. [Стриминговое управление](#стриминговое-управление)
6. [Программы и сценарии](#программы-и-сценарии)
7. [Обработка событий](#обработка-событий)
8. [Внешние устройства](#внешние-устройства)
9. [GPIO и I/O операции](#gpio-и-io-операции)
10. [Асинхронное программирование](#асинхронное-программирование)
11. [Обработка ошибок](#обработка-ошибок)

---

## Установка и быстрый старт

### Требования

- Python 3.12+
- Манипулятор и компьютер должны быть в одной сети

### Установка

```bash
# Установка из архива
pip install pm_python_sdk-0.6.7.tar.gz

# Или локальная установка
cd pm_python_sdk-0.6.7
pip install .
```

### Минимальный пример

```python
from sdk.manipulators.medu import MEdu

# Подключение к MEdu манипулятору
manipulator = MEdu(
    host="192.168.1.100",  # IP адрес манипулятора
    client_id="client_1",
    login="user",
    password="pass"
)

# Подключение
manipulator.connect()

# Получение управления
manipulator.get_control()

# Движение по углам
manipulator.move_to_angles(0.0, -0.5, -0.8)

# Отключение
manipulator.disconnect()
```

---

## Подключение к манипулятору

### Типы манипуляторов

SDK поддерживает два типа манипуляторов:

#### MEdu (3-осевой)

```python
from sdk.manipulators.medu import MEdu

manipulator = MEdu(
    host="192.168.1.100",
    client_id="client_1",
    login="user",
    password="pass"
)
```

#### M13 (6-осевой)

```python
from sdk.manipulators.m13 import M13

manipulator = M13(
    host="192.168.1.100",
    client_id="client_1",
    login="user",
    password="pass"
)
```

### Подключение и управление

```python
# Синхронное подключение
manipulator.connect()

# Получение управления (обязательно перед командами)
manipulator.get_control()

# Асинхронное подключение
import asyncio

async def connect_async():
    await manipulator.connect_async()
    await manipulator.get_control_async_await()

asyncio.run(connect_async())
```

### Отключение

```python
# Корректное отключение
manipulator.disconnect()
```

---

## Управление движением

### Движение по углам (MEdu)

```python
# Основные параметры
manipulator.move_to_angles(
    povorot_osnovaniya=0.0,   # Угол поворота основания (радианы)
    privod_plecha=-0.5,       # Угол плеча (радианы)
    privod_strely=-0.8,       # Угол стрелы (радианы)
    v_osnovaniya=0.0,         # Скорость основания (рад/с)
    v_plecha=0.0,             # Скорость плеча (рад/с)
    v_strely=0.0,             # Скорость стрелы (рад/с)
    velocity_factor=0.1,      # Множитель скорости 0.0-1.0
    acceleration_factor=0.1,  # Множитель ускорения 0.0-1.0
    timeout_seconds=60.0,     # Таймаут выполнения
    throw_error=True          # Бросать исключение при ошибке
)

# Движение без ожидания завершения
manipulator.move_to_angles_no_wait(0.0, -0.5, -0.8)

# Асинхронное движение
await manipulator.move_to_angles_async(0.0, -0.5, -0.8)
```

### Движение по углам (M13)

```python
# 6 степеней свободы
manipulator.move_to_angles(
    sp1=0.0,    # shoulder_pan_joint
    sp2=-1.57,  # shoulder_lift_joint
    sp3=1.57,   # elbow_joint
    sp4=0.0,    # wrist_1_joint
    sp5=0.0,    # wrist_2_joint
    sp6=0.0,    # wrist_3_joint
    sp1_v=0.0, sp2_v=0.0, sp3_v=0.0,
    sp4_v=0.0, sp5_v=0.0, sp6_v=0.0,
    velocity_factor=0.1,
    acceleration_factor=0.1
)
```

### Движение по координатам (Декартовы координаты)

```python
from sdk.commands.move_coordinates_command import (
    MoveCoordinatesParamsPosition,
    MoveCoordinatesParamsOrientation
)
from sdk.utils.enums import PlannerType

# Задание целевой позиции
position = MoveCoordinatesParamsPosition(
    x=0.3,   # метры
    y=0.0,
    z=0.2
)

# Задание ориентации (кватернион)
orientation = MoveCoordinatesParamsOrientation(
    x=0.0,
    y=0.0,
    z=0.0,
    w=1.0
)

# Движение
manipulator.move_to_coordinates(
    position=position,
    orientation=orientation,
    velocity_scaling_factor=0.1,      # 10% от макс. скорости
    acceleration_scaling_factor=0.1,  # 10% от макс. ускорения
    planner_type=PlannerType.LIN,     # Линейный планировщик
    timeout_seconds=30.0,
    throw_error=True
)
```

**Типы планировщиков:**
- `PlannerType.LIN` - линейное движение в декартовом пространстве
- `PlannerType.PTP` - движение точка-в-точку (может быть нелинейным)

### Движение по дуге

```python
from sdk.commands.arc_motion import Pose, Position, Orientation

# Целевая точка
target = Pose(
    position=Position(x=0.35, y=0.1, z=0.25),
    orientation=Orientation(x=0, y=0, z=0, w=1)
)

# Центр дуги
center_arc = Pose(
    position=Position(x=0.3, y=0.05, z=0.2),
    orientation=Orientation()
)

# Выполнение движения по дуге
manipulator.arc_motion(
    target=target,
    center_arc=center_arc,
    step=0.05,                           # Шаг интерполяции
    count_point_arc=50,                  # Количество точек на дуге
    max_velocity_scaling_factor=0.5,
    max_acceleration_scaling_factor=0.5,
    timeout_seconds=60.0,
    throw_error=True
)
```

### Палетирование (только M13)

```python
from sdk.commands.data import Pose, Position, Orientation

# Целевая позиция для палетирования
target_point = Pose(
    position=Position(x=0.4, y=0.2, z=0.3),
    orientation=Orientation(x=0, y=0, z=0, w=1)
)

# Фиксированная ориентация
hold_orientation = Orientation(x=0, y=0, z=0, w=1)

# Выполнение
manipulator.paletizing_movement(
    target_point=target_point,
    hold_orientation=hold_orientation,
    use_orientation=True,  # Использовать фиксированную ориентацию
    step=0.05,
    count_point=50,
    max_velocity_scaling_factor=0.1,
    max_acceleration_scaling_factor=0.1
)
```

### Остановка движения

```python
# Экстренная остановка
manipulator.stop_movement(timeout_seconds=5.0)

# Остановка без ожидания подтверждения
manipulator.stop_movement_no_wait()
```

### Получение текущей позиции

```python
# Получение координат
coordinates = manipulator.get_cartesian_coordinates()
print(coordinates)  # JSON строка с текущими координатами

# Получение состояния суставов
joints = manipulator.get_joint_state()
print(joints)  # JSON строка с углами суставов
```

---

## Работа с насадками

### Управление питанием насадок (MEdu)

```python
# Включить питание на стреле (обязательно перед использованием)
manipulator.nozzle_power(True)

# Выключить питание
manipulator.nozzle_power(False)

# Асинхронное управление
await manipulator.nozzle_power_async(True)
```

### Гриппер

#### Способ 1: Прямое управление через MEdu

```python
# Включить питание
manipulator.nozzle_power(True)

# Управление гриппером
manipulator.manage_gripper(
    rotation=20,   # Угол поворота насадки (градусы)
    gripper=10     # Угол раскрытия гриппера (градусы, 0=закрыт)
)

# Закрыть гриппер
manipulator.manage_gripper(rotation=0, gripper=0)

# Открыть гриппер
manipulator.manage_gripper(rotation=0, gripper=40)

# Асинхронно
await manipulator.manage_gripper_async(rotation=20, gripper=10)
```

#### Способ 2: Через класс GripperAttachment

```python
from sdk.manipulators.attachments.gripper import GripperAttachment

# Включить питание
manipulator.nozzle_power(True)

# Создание объекта гриппера (автоматически регистрируется)
gripper = GripperAttachment(
    manipulator,
    name="gripper",
    rotation_open=0,   # Угол в открытом состоянии
    gripper_open=40    # Раскрытие в открытом состоянии
)

# Закрыть гриппер (захватить)
gripper.activate(rotation=0, gripper=0)

# Открыть гриппер (отпустить)
gripper.deactivate()

# Проверка состояния
status = gripper.get_status()  # "active" или "idle"
```

### Вакуумная насадка

#### Способ 1: Прямое управление

```python
# Включить питание
manipulator.nozzle_power(True)

# Включить вакуум
manipulator.manage_vacuum(
    rotation=0,         # Угол поворота насадки
    power_supply=True   # Включить насос
)

# Выключить вакуум
manipulator.manage_vacuum(rotation=0, power_supply=False)

# Асинхронно
await manipulator.manage_vacuum_async(rotation=0, power_supply=True)
```

#### Способ 2: Через класс VacuumAttachment

```python
from sdk.manipulators.attachments.vacuum import VacuumAttachment

# Включить питание
manipulator.nozzle_power(True)

# Создание объекта вакуума
vacuum = VacuumAttachment(
    manipulator,
    name="vacuum",
    rotation=0
)

# Включить вакуум
vacuum.activate(rotation=0)

# Выключить вакуум
vacuum.deactivate()

# Проверка состояния
status = vacuum.get_status()
```

### Пример сборочной операции

```python
from sdk.manipulators.attachments.gripper import GripperAttachment
from sdk.commands.move_coordinates_command import (
    MoveCoordinatesParamsPosition,
    MoveCoordinatesParamsOrientation
)

# Инициализация
manipulator.connect()
manipulator.get_control()
manipulator.nozzle_power(True)

gripper = GripperAttachment(manipulator)

# Открыть гриппер
gripper.deactivate()

# Переместиться к детали
pos_pickup = MoveCoordinatesParamsPosition(0.3, 0.0, 0.15)
orient = MoveCoordinatesParamsOrientation(0, 0, 0, 1)
manipulator.move_to_coordinates(pos_pickup, orient, 0.1, 0.1)

# Захватить деталь
gripper.activate(rotation=0, gripper=0)

# Переместиться к месту установки
pos_place = MoveCoordinatesParamsPosition(0.35, 0.2, 0.2)
manipulator.move_to_coordinates(pos_place, orient, 0.1, 0.1)

# Отпустить деталь
gripper.deactivate()

# Вернуться в исходную позицию
manipulator.move_to_angles(0.0, 0.0, 0.0)

# Выключить питание
manipulator.nozzle_power(False)
```

---

## Стриминговое управление

Стриминг позволяет управлять манипулятором в режиме реального времени малыми шагами.

### Установка режима сервоуправления

```python
from sdk.utils.enums import ServoControlType

# Режим TWIST (управление скоростями)
manipulator.set_servo_twist_mode()

# Режим POSE (управление позицией)
manipulator.set_servo_pose_mode()

# Режим JOINT_JOG (управление углами)
manipulator.set_servo_joint_jog_mode()

# Универсальный способ
manipulator.set_servo_control_type(ServoControlType.TWIST)
```

### Стриминг скоростей (TWIST)

```python
import time

# Установить режим
manipulator.set_servo_twist_mode()

# Отправка команд скорости в цикле
for i in range(50):
    linear_vel = {"x": 0.02, "y": 0.0, "z": 0.0}
    angular_vel = {"rx": 0.0, "ry": 0.0, "rz": 0.01}
    
    manipulator.stream_cartesian_velocities(linear_vel, angular_vel)
    time.sleep(0.1)  # 10 Hz

# Остановка
manipulator.stream_cartesian_velocities(
    {"x": 0, "y": 0, "z": 0},
    {"rx": 0, "ry": 0, "rz": 0}
)
```

### Стриминг позиций (POSE)

```python
from sdk.commands.move_coordinates_command import (
    MoveCoordinatesParamsPosition,
    MoveCoordinatesParamsOrientation
)

# Установить режим
manipulator.set_servo_pose_mode()

# Стриминг целевых позиций
for i in range(100):
    x = 0.3 + i * 0.001  # Постепенное движение
    position = MoveCoordinatesParamsPosition(x, 0.0, 0.2)
    orientation = MoveCoordinatesParamsOrientation(0, 0, 0, 1)
    
    manipulator.stream_coordinates(position, orientation)
    time.sleep(0.05)  # 20 Hz
```

### Стриминг углов (JOINT_JOG)

#### MEdu

```python
# Установить режим
manipulator.set_servo_joint_jog_mode()

# Стриминг углов
for i in range(100):
    angle = i * 0.01
    manipulator.stream_joint_angles(
        povorot_osnovaniya=angle,
        privod_plecha=-0.5,
        privod_strely=-0.8,
        v_osnovaniya=0.1,
        v_plecha=0.1,
        v_strely=0.1
    )
    time.sleep(0.05)
```

#### M13

```python
# Установить режим
manipulator.set_servo_joint_jog_mode()

# Стриминг углов
for i in range(100):
    manipulator.stream_joint_angles(
        sp1=0.0, sp2=-1.57, sp3=1.57,
        sp4=0.0, sp5=0.0, sp6=0.0,
        v1=0.1, v2=0.1, v3=0.1,
        v4=0.1, v5=0.1, v6=0.1
    )
    time.sleep(0.05)
```

### Пример телеоперации

```python
import keyboard  # pip install keyboard
import time

manipulator.set_servo_twist_mode()

print("WASD - движение, Q/E - поворот, ESC - выход")

try:
    while True:
        linear = {"x": 0.0, "y": 0.0, "z": 0.0}
        angular = {"rx": 0.0, "ry": 0.0, "rz": 0.0}
        
        if keyboard.is_pressed('w'):
            linear["x"] = 0.05
        if keyboard.is_pressed('s'):
            linear["x"] = -0.05
        if keyboard.is_pressed('a'):
            linear["y"] = 0.05
        if keyboard.is_pressed('d'):
            linear["y"] = -0.05
        if keyboard.is_pressed('q'):
            angular["rz"] = 0.1
        if keyboard.is_pressed('e'):
            angular["rz"] = -0.1
        if keyboard.is_pressed('esc'):
            break
        
        manipulator.stream_cartesian_velocities(linear, angular)
        time.sleep(0.1)
finally:
    # Остановка
    manipulator.stream_cartesian_velocities(
        {"x": 0, "y": 0, "z": 0},
        {"rx": 0, "ry": 0, "rz": 0}
    )
```

---

## Программы и сценарии

### Запуск готовой программы

```python
# Запуск программы по имени
manipulator.run_program_by_name('edum/default')

# С обработкой ошибок
try:
    manipulator.run_program_by_name(
        program_name='my_program',
        timeout_seconds=120.0,
        throw_error=True
    )
except Exception as e:
    print(f"Ошибка выполнения программы: {e}")
```

### Запуск JSON программы

```python
# Определение программы в формате JSON
program_json = {
    'Root': [
        {
            'Move': {
                'content': [
                    {
                        'Point': {
                            'positions': [0.3, -0.3, -0.4],
                            'time': 0.5
                        }
                    },
                    {
                        'Point': {
                            'positions': [0.0, 0.0, 0.0],
                            'time': 1.0
                        }
                    }
                ],
                'type': 'Simple'
            }
        }
    ]
}

# Запуск
manipulator.run_program_json(
    name='my_json_program',
    program_json=program_json,
    timeout_seconds=60.0
)
```

### Выполнение Python кода на роботе

```python
# Простой код
python_code = """
print('Hello from robot!')
import time
for i in range(5):
    print(f'Iteration {i}')
    time.sleep(1)
"""

manipulator.run_python_program(python_code)

# С зависимостями
python_code = """
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(f'Array sum: {arr.sum()}')
"""

manipulator.run_python_program(
    python_code=python_code,
    env_name="my_env",
    python_version="3.12",
    requirements=["numpy>=1.20.0"],
    timeout_seconds=120.0
)
```

### Программы без ожидания

```python
# Запуск без блокировки
manipulator.run_program_by_name_no_wait('background_program')

# Продолжение работы
manipulator.move_to_angles(0.0, 0.0, 0.0)

# Python код без ожидания
manipulator.run_python_program_no_wait("print('Background task')")
```

---

## Обработка событий

### Способ 1: Установка обработчиков

```python
import json

# Обработчик координат
def on_coordinates(data):
    position = data.get('position', {})
    print(f"X: {position.get('x')}, Y: {position.get('y')}, Z: {position.get('z')}")

# Обработчик состояния суставов
def on_joints(data):
    positions = data.get('position', {})
    print(f"Углы: {positions}")

# Обработчик ошибок
def on_error(data):
    error_type = data.get('type')
    message = data.get('message')
    print(f"Ошибка {error_type}: {message}")

# Регистрация обработчиков
manipulator.set_coordinates_handler(on_coordinates)
manipulator.set_joint_states_handler(on_joints)
manipulator.set_hardware_error_handler(on_error)

# Основной код программы
manipulator.connect()
manipulator.get_control()
manipulator.move_to_angles(0.0, -0.5, -0.8)

# События будут обрабатываться автоматически
import time
time.sleep(5)

# Отписка от событий
manipulator.unsubscribe_from_topic("/coordinates")
```

### Способ 2: Декораторы

```python
# Декоратор для координат
@manipulator.on_coordinates()
def handle_coordinates(data):
    print(f"Координаты обновлены: {data}")

# Декоратор для GPIO
@manipulator.on_gpio_states()
def handle_gpio(data):
    print(f"GPIO изменилось: {data}")

# Декоратор для произвольного топика
@manipulator.on_topic("/custom_topic")
def handle_custom(data):
    print(f"Получено: {data}")
```

### Способ 3: Универсальный обработчик

```python
import json

def message_handler(topic, payload):
    """Обработчик всех входящих сообщений"""
    data = json.loads(payload)
    
    if topic == "/coordinates":
        print(f"Координаты: {data}")
    elif topic == "/joint_states":
        print(f"Суставы: {data}")
    elif topic == "/hardware_error":
        print(f"ОШИБКА: {data}")

# Установка обработчика
manipulator.on_message = message_handler

# Все сообщения будут проходить через message_handler
```

### Подписка на состояние суставов (MEdu/M13)

```python
def joint_callback(joint_data):
    """Вызывается при обновлении состояния суставов"""
    positions = joint_data.get('position', {})
    velocities = joint_data.get('velocity', {})
    
    print("Текущие углы:", positions)
    print("Текущие скорости:", velocities)

# Подписка
manipulator.subscribe_to_joint_state(joint_callback)

# Работа программы...
import time
time.sleep(10)

# Отписка
manipulator.unsubscribe_from_joint_state()
```

### Доступные топики событий

| Топик | Описание | Метод подписки |
|-------|----------|----------------|
| `/coordinates` | Текущие координаты | `set_coordinates_handler()` |
| `/joint_states` | Состояние суставов | `set_joint_states_handler()` |
| `/gpio_states` | Состояние GPIO | `set_gpio_states_handler()` |
| `/gamepad_info` | Данные с геймпада | `set_gamepad_info_handler()` |
| `/hardware_state` | Состояние железа | `set_hardware_state_handler()` |
| `/hardware_error` | Аппаратные ошибки | `set_hardware_error_handler()` |
| `/manipulator_info` | Информация о манипуляторе | `set_manipulator_info_handler()` |

---

## Внешние устройства

### MGbot Конвейер

```python
# Управление скоростью моторов (0-100)
manipulator.mgbot_conveyer.set_speed_motors(50)

# Остановка
manipulator.mgbot_conveyer.set_speed_motors(0)

# Управление сервоприводом (угол 0-180)
manipulator.mgbot_conveyer.set_servo_angle(90)

# Управление светодиодом (RGB 0-255)
manipulator.mgbot_conveyer.set_led_color(r=255, g=0, b=0)  # Красный
manipulator.mgbot_conveyer.set_led_color(0, 255, 0)        # Зеленый

# Вывод текста на дисплей
manipulator.mgbot_conveyer.display_text("Hello Robot!")

# Звуковой сигнал (тон 1-15)
manipulator.mgbot_conveyer.set_buzz_tone(10)

# Чтение датчиков
sensor_data = manipulator.mgbot_conveyer.get_sensors_data(enabled=True)
print(f"Дистанция: {sensor_data.get('DistanceSensor')}")
print(f"Цвет: {sensor_data.get('ColorSensor')}")
print(f"Приближение: {sensor_data.get('Prox')}")

# Асинхронное использование
await manipulator.mgbot_conveyer.set_speed_motors_async(30)
```

### Пример конвейерной сортировки

```python
from sdk.manipulators.attachments.vacuum import VacuumAttachment

# Инициализация
manipulator.connect()
manipulator.get_control()
manipulator.nozzle_power(True)
vacuum = VacuumAttachment(manipulator)

# Запуск конвейера
manipulator.mgbot_conveyer.set_speed_motors(30)

while True:
    # Чтение датчиков
    sensors = manipulator.mgbot_conveyer.get_sensors_data(True)
    distance = sensors.get('DistanceSensor', 100)
    
    if distance < 10:  # Деталь обнаружена
        # Остановка конвейера
        manipulator.mgbot_conveyer.set_speed_motors(0)
        
        # Взять деталь
        vacuum.activate()
        
        # Переместить
        manipulator.move_to_angles(0.5, -0.3, -0.5)
        
        # Отпустить
        vacuum.deactivate()
        
        # Вернуться
        manipulator.move_to_angles(0.0, 0.0, 0.0)
        
        # Продолжить конвейер
        manipulator.mgbot_conveyer.set_speed_motors(30)
    
    time.sleep(0.1)
```

### PixyCam (UART)

```python
# Получение версии камеры
version = manipulator.pixy_cam_uart_control.get_version()
print(f"Версия PixyCam: {version}")

# Получение разрешения
resolution = manipulator.pixy_cam_uart_control.get_resolution_uart(type=0)
print(f"Разрешение: {resolution}")

# Получение FPS
fps = manipulator.pixy_cam_uart_control.get_fps_uart()
print(f"FPS: {fps}")

# Установка яркости (0-255)
manipulator.pixy_cam_uart_control.set_camera_brightness_uart(128)

# Управление сервоприводами камеры
manipulator.pixy_cam_uart_control.set_servos_uart(s0=100, s1=150)

# Управление светодиодом
manipulator.pixy_cam_uart_control.set_led_uart(r=255, g=0, b=0)

# Получение координат объекта
coordinates = manipulator.get_block_coordinates_from_pixy(
    signature=1  # ID подписи объекта
)
print(f"Координаты: {coordinates}")
```

### Конвейер: управление скоростью

```python
# Установка скорости конвейера (скалярное значение)
manipulator.set_conveyer_velocity(0.5)  # 50%

# Остановка
manipulator.set_conveyer_velocity(0.0)

# Асинхронно
await manipulator.set_conveyer_velocity_async(0.3)
```

### Калибровка линейного модуля

```python
# Калибровка контроллера линейного модуля
manipulator.calibrate_controller(timeout_seconds=120.0)

# Движение линейного модуля
manipulator.move_linear_module(
    distance=0.5,  # метры
    timeout_seconds=30.0
)

# Асинхронно
await manipulator.move_linear_module_async(0.5)
```

---

## GPIO и I/O операции

### Цифровые выходы

```python
# Запись в цифровой выход (канал 0-7, значение True/False)
manipulator.write_digital_output(channel=0, value=True)
manipulator.write_digital_output(channel=0, value=False)

# Без ожидания
manipulator.write_digital_output_no_wait(channel=1, value=True)

# Асинхронно
await manipulator.write_digital_output_async(channel=2, value=True)
```

### Аналоговые выходы

```python
# Запись в аналоговый выход (канал 0-3, значение 0.0-1.0)
manipulator.write_analog_output(channel=0, value=0.5)  # 50%
manipulator.write_analog_output(channel=1, value=1.0)  # 100%

# Без ожидания
manipulator.write_analog_output_no_wait(channel=0, value=0.75)

# Асинхронно
await manipulator.write_analog_output_async(channel=0, value=0.3)
```

### GPIO управление

```python
# Запись в GPIO (name - путь к GPIO, value - 0 или 1)
gpio_name = "/dev/gpiochip4/e1_pin"

manipulator.write_gpio(
    name=gpio_name,
    value=1,
    timeout_seconds=1.0,
    throw_error=True
)

# Выключить
manipulator.write_gpio(gpio_name, 0)

# Чтение GPIO
value = manipulator.get_gpio_value(gpio_name)
print(f"GPIO значение: {value}")
```

### GPIO маски (M13)

```python
# Установка значений по маске
manipulator.set_gpio_on_mask(
    name="gpio_bank_1",
    value_mask="10101010"  # Бинарная маска
)

# Получение маски
mask_data = manipulator.get_gpio_mask("gpio_bank_1")
print(f"Маска: {mask_data}")

# Асинхронно
await manipulator.set_gpio_on_mask_async("gpio_bank_1", "11110000")
```

### I2C операции (MEdu)

```python
# Запись в I2C
manipulator.write_i2c(
    name="i2c_device_address",
    value=0x42,
    timeout_seconds=5.0
)

# Чтение из I2C
value = manipulator.get_i2c_value("i2c_device_address")
print(f"I2C значение: {value}")

# Асинхронно
await manipulator.write_i2c_async("i2c_device_address", 0x55)
```

### Пример управления светодиодом

```python
import time

gpio_led = "/dev/gpiochip4/led_pin"

def blink_led(times=5):
    for _ in range(times):
        manipulator.write_gpio(gpio_led, 1)
        time.sleep(0.5)
        manipulator.write_gpio(gpio_led, 0)
        time.sleep(0.5)

blink_led(10)
```

---

## Асинхронное программирование

SDK поддерживает полноценное асинхронное программирование с использованием `asyncio`.

### Базовое использование

```python
import asyncio
from sdk.manipulators.medu import MEdu

async def main():
    manipulator = MEdu("192.168.1.100", "client_1", "user", "pass")
    
    # Асинхронное подключение
    await manipulator.connect_async()
    await manipulator.get_control_async_await()
    
    # Асинхронные движения
    await manipulator.move_to_angles_async(0.0, -0.5, -0.8)
    await manipulator.move_to_angles_async(0.0, 0.0, 0.0)
    
    manipulator.disconnect()

# Запуск
asyncio.run(main())
```

### Параллельное выполнение

```python
async def main():
    manipulator = MEdu("192.168.1.100", "client_1", "user", "pass")
    await manipulator.connect_async()
    await manipulator.get_control_async_await()
    
    # Создание задач
    task1 = asyncio.create_task(
        manipulator.nozzle_power_async(True)
    )
    task2 = asyncio.create_task(
        manipulator.mgbot_conveyer.set_speed_motors_async(50)
    )
    
    # Ожидание завершения всех задач
    await asyncio.gather(task1, task2)
    
    # Последовательность движений
    await manipulator.move_to_angles_async(0.0, -0.5, -0.8)
    await manipulator.manage_gripper_async(rotation=0, gripper=0)
    
    manipulator.disconnect()

asyncio.run(main())
```

### Асинхронная обработка событий

```python
async def monitor_coordinates(manipulator):
    """Асинхронный мониторинг координат"""
    while True:
        coords = await manipulator.get_cartesian_coordinates_async_await()
        print(f"Координаты: {coords}")
        await asyncio.sleep(0.5)

async def perform_movements(manipulator):
    """Выполнение движений"""
    for i in range(5):
        await manipulator.move_to_angles_async(0.0, -0.5 + i*0.1, -0.8)
        await asyncio.sleep(1)

async def main():
    manipulator = MEdu("192.168.1.100", "client_1", "user", "pass")
    await manipulator.connect_async()
    await manipulator.get_control_async_await()
    
    # Параллельный запуск мониторинга и движений
    monitor_task = asyncio.create_task(monitor_coordinates(manipulator))
    movement_task = asyncio.create_task(perform_movements(manipulator))
    
    # Ждем завершения движений
    await movement_task
    
    # Отменяем мониторинг
    monitor_task.cancel()
    
    manipulator.disconnect()

asyncio.run(main())
```

### Асинхронный стриминг

```python
async def async_streaming():
    manipulator = MEdu("192.168.1.100", "client_1", "user", "pass")
    await manipulator.connect_async()
    await manipulator.get_control_async_await()
    
    manipulator.set_servo_twist_mode()
    
    # Асинхронный стриминг
    for i in range(100):
        linear = {"x": 0.02, "y": 0.0, "z": 0.0}
        angular = {"rx": 0.0, "ry": 0.0, "rz": 0.0}
        
        await manipulator.stream_cartesian_velocities_async(linear, angular)
        await asyncio.sleep(0.05)
    
    # Остановка
    await manipulator.stream_cartesian_velocities_async(
        {"x": 0, "y": 0, "z": 0},
        {"rx": 0, "ry": 0, "rz": 0}
    )
    
    manipulator.disconnect()

asyncio.run(async_streaming())
```

---

## Обработка ошибок

### Базовая обработка

```python
try:
    manipulator.connect()
    manipulator.get_control()
    manipulator.move_to_angles(0.0, -0.5, -0.8)
except Exception as e:
    print(f"Ошибка: {e}")
    manipulator.stop_movement()
finally:
    manipulator.disconnect()
```

### Таймауты

```python
# Все команды поддерживают параметр timeout_seconds
try:
    manipulator.move_to_coordinates(
        position,
        orientation,
        0.1, 0.1,
        timeout_seconds=10.0,  # Максимум 10 секунд
        throw_error=True
    )
except TimeoutError:
    print("Команда превысила таймаут")
    manipulator.stop_movement()
```

### Отключение исключений

```python
# throw_error=False - не бросать исключения
result = manipulator.move_to_angles(
    0.0, -0.5, -0.8,
    throw_error=False
)

# Проверка результата
if result and result.get('success'):
    print("Успешно")
else:
    print("Ошибка:", result.get('error'))
```

### Обработка аппаратных ошибок

```python
def hardware_error_handler(error_data):
    """Обработчик аппаратных ошибок"""
    error_type = error_data.get('type')
    message = error_data.get('message')
    
    print(f"Аппаратная ошибка {error_type}: {message}")
    
    # Остановка при критических ошибках
    if error_type in [4, 6]:  # EMERGENCY_STOP, ERROR
        manipulator.stop_movement()
        manipulator.change_state(ManipulatorState.IDLE)

# Регистрация обработчика
manipulator.set_hardware_error_handler(hardware_error_handler)
```

### Состояния манипулятора

```python
from sdk.utils.enums import ManipulatorState

# Установка состояния
manipulator.change_state(ManipulatorState.IDLE)
manipulator.change_state(ManipulatorState.AUTO)
manipulator.change_state(ManipulatorState.MANUAL)
manipulator.change_state(ManipulatorState.EMERGENCY_STOP)

# Доступные состояния:
# - IDLE (0): Простой
# - AUTO (1): Автоматический режим
# - MANUAL (2): Ручной режим
# - CALIBRATION (3): Калибровка
# - EMERGENCY_STOP (4): Аварийная остановка
# - TEACHING (5): Обучение
# - ERROR (6): Ошибка
# - ACTIVE_REAL (7): Активен
```

### Ограничения суставов

```python
from sdk.commands.manipulator_commands import JointLimit

# Получение текущих ограничений
limits = manipulator.get_joint_limits()

# Установка новых ограничений
new_limits = [
    JointLimit(
        joint_name="povorot_osnovaniya",
        min_position=-3.14,
        max_position=3.14,
        max_velocity=2.0,
        max_acceleration=5.0
    ),
    JointLimit(
        joint_name="privod_plecha",
        min_position=-1.57,
        max_position=1.57,
        max_velocity=1.5,
        max_acceleration=3.0
    )
]

manipulator.set_joint_limits(new_limits)
```

### Очистка команд

```python
# Принудительная очистка всех активных команд
manipulator.clear_all_commands()

# Очистка всех обработчиков событий
manipulator.clear_all_handlers()

# Отписка от потоковых топиков
manipulator.unsubscribe_from_streaming_topics()
```

---

## Полные примеры

### Пример 1: Pick and Place

```python
from sdk.manipulators.medu import MEdu
from sdk.manipulators.attachments.gripper import GripperAttachment
from sdk.commands.move_coordinates_command import (
    MoveCoordinatesParamsPosition,
    MoveCoordinatesParamsOrientation
)

def pick_and_place():
    # Инициализация
    manipulator = MEdu("192.168.1.100", "client", "user", "pass")
    manipulator.connect()
    manipulator.get_control()
    
    # Включение питания и настройка гриппера
    manipulator.nozzle_power(True)
    gripper = GripperAttachment(manipulator)
    
    try:
        # Позиции
        home_pos = MoveCoordinatesParamsPosition(0.25, 0.0, 0.3)
        pickup_pos = MoveCoordinatesParamsPosition(0.35, 0.05, 0.15)
        place_pos = MoveCoordinatesParamsPosition(0.35, -0.05, 0.15)
        orientation = MoveCoordinatesParamsOrientation(0, 0, 0, 1)
        
        # Открыть гриппер
        gripper.deactivate()
        
        # Движение к точке захвата
        manipulator.move_to_coordinates(pickup_pos, orientation, 0.2, 0.2)
        
        # Захват
        gripper.activate(rotation=0, gripper=0)
        import time
        time.sleep(0.5)
        
        # Подъем
        manipulator.move_to_coordinates(home_pos, orientation, 0.2, 0.2)
        
        # Движение к точке размещения
        manipulator.move_to_coordinates(place_pos, orientation, 0.2, 0.2)
        
        # Освобождение
        gripper.deactivate()
        time.sleep(0.5)
        
        # Возврат домой
        manipulator.move_to_coordinates(home_pos, orientation, 0.2, 0.2)
        
    finally:
        # Очистка
        manipulator.nozzle_power(False)
        manipulator.disconnect()

if __name__ == "__main__":
    pick_and_place()
```

### Пример 2: Конвейерная сортировка с PixyCam

```python
import asyncio
from sdk.manipulators.medu import MEdu
from sdk.manipulators.attachments.vacuum import VacuumAttachment

async def conveyor_sorting():
    manipulator = MEdu("192.168.1.100", "client", "user", "pass")
    await manipulator.connect_async()
    await manipulator.get_control_async_await()
    
    # Инициализация
    await manipulator.nozzle_power_async(True)
    vacuum = VacuumAttachment(manipulator)
    
    # Запуск конвейера
    await manipulator.mgbot_conveyer.set_speed_motors_async(40)
    
    try:
        while True:
            # Чтение датчиков
            sensors = await manipulator.mgbot_conveyer.get_sensors_data_async(True)
            distance = sensors.get('DistanceSensor', 100)
            color = sensors.get('ColorSensor', {})
            
            if distance < 15:  # Деталь обнаружена
                # Остановка конвейера
                await manipulator.mgbot_conveyer.set_speed_motors_async(0)
                
                # Распознавание объекта камерой
                coords = manipulator.get_block_coordinates_from_pixy(signature=1)
                
                # Взять деталь
                vacuum.activate()
                await asyncio.sleep(0.3)
                
                # Сортировка по цвету
                if color.get('R', 0) > 200:  # Красный
                    await manipulator.move_to_angles_async(0.5, -0.4, -0.6)
                else:  # Другой
                    await manipulator.move_to_angles_async(-0.5, -0.4, -0.6)
                
                # Отпустить
                vacuum.deactivate()
                await asyncio.sleep(0.3)
                
                # Вернуться
                await manipulator.move_to_angles_async(0.0, 0.0, 0.0)
                
                # Продолжить конвейер
                await manipulator.mgbot_conveyer.set_speed_motors_async(40)
            
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Остановка...")
    finally:
        await manipulator.mgbot_conveyer.set_speed_motors_async(0)
        await manipulator.nozzle_power_async(False)
        manipulator.disconnect()

if __name__ == "__main__":
    asyncio.run(conveyor_sorting())
```

### Пример 3: Телеоперация с событиями

```python
import keyboard
import time
from sdk.manipulators.medu import MEdu

def teleoperation():
    manipulator = MEdu("192.168.1.100", "client", "user", "pass")
    manipulator.connect()
    manipulator.get_control()
    
    # Обработчик координат для отображения
    def show_position(data):
        pos = data.get('position', {})
        print(f"\rX:{pos.get('x', 0):.3f} Y:{pos.get('y', 0):.3f} Z:{pos.get('z', 0):.3f}", end='')
    
    manipulator.set_coordinates_handler(show_position)
    
    # Включение режима стриминга
    manipulator.set_servo_twist_mode()
    
    print("Управление: WASD - движение, Q/E - вращение, Space - стоп, ESC - выход")
    
    try:
        while True:
            linear = {"x": 0.0, "y": 0.0, "z": 0.0}
            angular = {"rx": 0.0, "ry": 0.0, "rz": 0.0}
            
            speed = 0.05
            
            if keyboard.is_pressed('w'):
                linear["x"] = speed
            if keyboard.is_pressed('s'):
                linear["x"] = -speed
            if keyboard.is_pressed('a'):
                linear["y"] = speed
            if keyboard.is_pressed('d'):
                linear["y"] = -speed
            if keyboard.is_pressed('q'):
                angular["rz"] = 0.2
            if keyboard.is_pressed('e'):
                angular["rz"] = -0.2
            if keyboard.is_pressed('space'):
                linear = {"x": 0, "y": 0, "z": 0}
                angular = {"rx": 0, "ry": 0, "rz": 0}
            if keyboard.is_pressed('esc'):
                break
            
            manipulator.stream_cartesian_velocities(linear, angular)
            time.sleep(0.05)
            
    finally:
        # Остановка
        manipulator.stream_cartesian_velocities(
            {"x": 0, "y": 0, "z": 0},
            {"rx": 0, "ry": 0, "rz": 0}
        )
        manipulator.disconnect()

if __name__ == "__main__":
    teleoperation()
```

---

## Дополнительная информация

### Системные требования

- Python 3.12+
- Библиотека paho-mqtt >= 2.1.0
- Стабильное сетевое подключение (Wi-Fi или Ethernet)

### Сетевая конфигурация

Определение IP-адреса манипулятора:
```bash
# На манипуляторе выполните:
ip a
```

Проверка связи:
```bash
# На компьютере:
ping 192.168.1.100
```

### Протокол связи

SDK использует протокол MQTT для связи с манипулятором:
- **Порт:** 1883 (стандартный MQTT)
- **Топики:** `/commands`, `/coordinates`, `/joint_states`, и др.
- **QoS:** 1 (гарантированная доставка)

### Производительность

- Стриминг: рекомендуется частота 10-20 Hz
- Команды движения: время выполнения зависит от расстояния и скорости
- Сетевая задержка: обычно < 10 мс в локальной сети

### Безопасность

```python
# Аварийная остановка
manipulator.stop_movement()
manipulator.change_state(ManipulatorState.EMERGENCY_STOP)

# Установка мягких ограничений
from sdk.commands.manipulator_commands import JointLimit

safe_limits = [
    JointLimit("povorot_osnovaniya", -2.0, 2.0, 1.0, 2.0),
    JointLimit("privod_plecha", -1.0, 1.0, 0.8, 1.5),
    JointLimit("privod_strely", -1.5, 0.5, 0.8, 1.5)
]
manipulator.set_joint_limits(safe_limits)
```

### Отладка

```python
# Включение подробного логирования (в коде SDK)
import logging
logging.basicConfig(level=logging.DEBUG)

# Мониторинг всех сообщений MQTT
def debug_handler(topic, payload):
    print(f"[DEBUG] {topic}: {payload}")

manipulator.on_message = debug_handler
```

### Поддержка и документация

- **SDK Guide:** `SDK_GUIDE.md` в корне проекта
- **README:** `README.md` с быстрыми примерами
- **Официальный сайт:** https://promo-bot.ru/promobot-m-edu/
- **Email поддержки:** info@promo-bot.ru

---

© 2024 ПРОМОБОТ. Версия SDK: 0.6.7

