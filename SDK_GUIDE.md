# SDK: Управление манипулятором с помощью Python — ПРОМОБОТ

Документация по использованию Python SDK для манипуляторов ПРОМОБОТ.

## Содержание
- [SDK: Управление манипулятором с помощью Python — ПРОМОБОТ](#sdk-управление-манипулятором-с-помощью-python--промобот)
  - [Содержание](#содержание)
  - [1. Введение и Обзор](#1-введение-и-обзор)
    - [Проверка версии](#проверка-версии)
    - [Установка](#установка)
    - [Виртуальное окружение](#виртуальное-окружение)
  - [2. Описание архитектуры программного обеспечения](#2-описание-архитектуры-программного-обеспечения)
  - [3. Типы команд](#3-типы-команд)
  - [4. Программные блоки (Структура программы)](#4-программные-блоки-структура-программы)
  - [5. Примеры движений](#5-примеры-движений)
    - [5.1 Движение по углам](#51-движение-по-углам)
    - [5.2 Движение по координатам](#52-движение-по-координатам)
    - [5.3 Движение по дуге](#53-движение-по-дуге)
  - [6. Работа с насадками](#6-работа-с-насадками)
  - [7. Стриминг](#7-стриминг)
  - [8. Программы](#8-программы)
  - [9. Остановка движениями](#9-остановка-движениями)
  - [10. Состояния и данные](#10-состояния-и-данные)
  - [11. Конвейерная лента (MGbot)](#11-конвейерная-лента-mgbot)
  - [12. Управление GPIO](#12-управление-gpio)
  - [Примеры использования команд](#примеры-использования-команд)
  - [Заключение](#заключение)

---

## 1. Введение и Обзор

Python SDK — библиотека от «ПРОМОБОТ» для программного управления манипуляторами через приложение M Control. SDK позволяет отправлять команды и получать обратную связь от робота. Библиотека бесплатна и устанавливается на ПК.

> **Требование к сети:** манипулятор и компьютер должны быть доступны друг другу по сети (локально или через Интернет).  
> **Требование к Python:** используйте Python **3.12**, создайте виртуальное окружение.

### Проверка версии
```bash
python3.12 --version
# или
python --version
```

### Установка
**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-distutils
```

**macOS (Homebrew):**
```bash
brew update
brew install python@3.12
```

**Windows (PowerShell после установки с python.org):**
```powershell
python --version
```

**pyenv (по желанию):**
```bash
curl https://pyenv.run | bash
pyenv install 3.12.0
pyenv global 3.12.0
```

### Виртуальное окружение
```bash
python3.12 -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

---

## 2. Описание архитектуры программного обеспечения

Доступны два способа программирования: визуальный (Blockly) и через SDK. Взаимодействие реализовано по модели клиент‑сервер через **MQTT**.



**Ключевые компоненты:**
- **Клиент:** ПК пользователя / приложение с SDK.
- **Сервер (`pm_develop_api`):** на манипуляторе, обрабатывает команды.
- **M Control:** приложение, переводит действия GUI в ROS2/rosbridge команды.

Сервер принимает команды, возвращает ответы и ведет стриминг текущих декартовых координат и состояния суставов.

---

## 3. Типы команд

- **Синхронные** — выполняются последовательно и блокируют поток: `manipulator.get_control()`
- **Асинхронные** — имеют суффикс `_async` и await‑варианты.
- **Стриминговые** — управление малыми шагами (скорости, позы, суставы).
- **`no_wait`** — асинхронно без ожидания результата.

**Примеры:**
```python
# синхронный
manipulator.get_control()

# асинхронный (awaitable)
await manipulator.get_control_async_await()

# стриминговый (псевдокод)
for i in range(5):
    manipulator.stream_cartesian_velocities(lin, ang)
    time.sleep(0.1)

# no_wait
manipulator.get_control_no_wait()
```

> В примерах далее используются синхронные методы.

---

## 4. Программные блоки (Структура программы)

1) Импорты.  
2) Подключение к манипулятору и захват управления.  
3) Основной блок (движения, чтение данных).  
4) Завершающий блок.

**Минимальный пример:**
```python
from sdk.manipulators.medu import MEdu

host = "192.168.88.182"  # IP манипулятора
client_id = "122"
login = "13"
password = "14"

manipulator = MEdu(host, client_id, login, password)
manipulator.connect()
manipulator.get_control()
```

---

## 5. Примеры движений

### 5.1 Движение по углам
```python
manipulator.move_to_angles(0.05, -0.35, -0.75)
```

### 5.2 Движение по координатам
```python
from sdk.commands.move_coordinates_command import (
    MoveCoordinatesParamsPosition,
    MoveCoordinatesParamsOrientation,
)
from sdk.utils.enums import PlannerType

position = MoveCoordinatesParamsPosition(0.32, -0.004, 0.25)
orientation = MoveCoordinatesParamsOrientation(0, 0, 0, 1.0)

manipulator.move_to_coordinates(
    position,
    orientation,
    velocity_scaling_factor=0.1,
    acceleration_scaling_factor=0.1,
    planner_type=PlannerType.LIN,
    timeout_seconds=30.0,
    throw_error=True,
)
```

**Параметры:**
- `position`: объект с `x, y, z`
- `orientation`: объект с `x, y, z, w`
- `velocity_scaling_factor`: доля от max скорости, по умолчанию `0.1`
- `acceleration_scaling_factor`: доля от max ускорения, по умолчанию `0.1`
- `planner_type`: тип планировщика, по умолчанию `PlannerType.LIN`
- `timeout_seconds`: таймаут
- `throw_error`: кидать исключение при ошибке

### 5.3 Движение по дуге
```python
from sdk.commands.arc_motion import ArcMotion, Pose, Position, Orientation

target = Pose(position=Position(target_x, target_y, target_z), orientation=Orientation())
center_arc = Pose(position=Position(center_x, center_y, center_z), orientation=Orientation())

manipulator.arc_motion(
    target,
    center_arc,
    step=0.05,
    count_point_arc=50,
    max_velocity_scaling_factor=0.5,
    max_acceleration_scaling_factor=0.5,
)
```

**Параметры:** `target`, `center_arc`, `step`, `count_point_arc`, `max_velocity_scaling_factor`, `max_acceleration_scaling_factor`, `timeout_seconds`, `throw_error`.

---

## 6. Работа с насадками

**Насадка:** *Gripper* — механический захват.  
Перед активацией включите питание: `manipulator.nozzle_power(True)`.

**Варианты:**
1. **Прямой контроль** через `GripperAttachment` (`activate`/`deactivate`).
2. **Через манипулятор**: `manipulator.manage_gripper(rotation=..., gripper=...)`.

```python
# Прямой
manipulator.nozzle_power(True)
gripper = GripperAttachment(manipulator)
gripper.activate(rotation=20, gripper=10)
gripper.deactivate()

# Через манипулятор
manipulator.nozzle_power(True)
manipulator.manage_gripper(rotation=20, gripper=10)
```

**Параметры `activate`:**
- `rotation` — градусы
- `gripper` — градусы

---

## 7. Стриминг

Режимы: **TWIST** (скорости), **POSE** (поза), **JOINT_JOG** (углы суставов).  
Перед началом включите режим.

```python
from sdk.utils.enums import ServoControlType

manipulator.set_servo_control_type(ServoControlType.TWIST)
manipulator.set_servo_twist_mode()
manipulator.set_servo_pose_mode()
manipulator.set_servo_joint_jog_mode()
```

**Скорости (TWIST):**
```python
manipulator.set_servo_twist_mode()
linear_vel = {"x": 0.02, "y": 0, "z": 0}
angular_vel = {"rx": 0, "ry": 0, "rz": 0.01}
manipulator.stream_cartesian_velocities(linear_vel, angular_vel)
```

**Поза (POSE):**
```python
position = MoveCoordinatesParamsPosition(0.27, 0.0, 0.15)
orientation = MoveCoordinatesParamsOrientation(0, 0, 0, 1)
manipulator.stream_coordinates(position, orientation)
```

**Суставы (JOINT_JOG):**
```python
manipulator.set_servo_joint_jog_mode()
manipulator.stream_joint_angles(
    povorot_osnovaniya=0.5, privod_plecha=1.0, privod_strely=0.8,
    v_osnovaniya=0.2, v_plecha=0.1, v_strely=0.15,
)
```

---

## 8. Программы

Запуск готовых программ, JSON‑сценариев и Python‑кода на роботе.

```python
# Готовая программа
manipulator.run_program('edum/default')

# JSON‑программа
program_json = {
  'Root':[{'Move':{'content':[{'Point':{'positions':[0.3,-0.3,-0.4],'time':0.5}}],'type':'Simple'}}]
}
manipulator.run_program_json('program_1', program_json)

# Python‑код на роботе
manipulator.run_python_program("print('Hello!')")
```

---

## 9. Остановка движениями
```python
manipulator.stop_movement(timeout_seconds=5.0)
```

---

## 10. Состояния и данные

Методы:
- `manipulator.get_joint_state()`
- `manipulator.get_home_position()`
- `manipulator.get_cartesian_coordinates()`
- `manipulator.subscribe_coordinates()`
- `manipulator.subscribe_hardware_error()`

Ошибки: JSON вида `{"type": id, "message": "..."}`.

---

## 11. Конвейерная лента (MGbot)

```python
# Скорость мотора (0..100)
manipulator.mgbot_conveyer.set_speed_motors(10)
# Угол сервопривода
manipulator.mgbot_conveyer.set_servo_angle(45)
# Цвет светодиода (0..255)
manipulator.mgbot_conveyer.set_led_color(255, 0, 0)
# Текст на дисплее
manipulator.mgbot_conveyer.display_text('Hello')
# Звуковой сигнал (1..15)
manipulator.mgbot_conveyer.set_buzz_tone(10)
# Датчики
sensor_data = manipulator.mgbot_conveyer.get_sensors_data(True)
# -> поля: "DistanceSensor", "ColorSensor", "Prox"
```

**Параметры и данные:** см. комментарии к методам выше.

**Индикация:**
- **LED1 (синий):** питание 5 В через USB.
- **LED2 (красный):** питание 8–30 В.
- **LED3 (розовый):** управляется через GPIO4 (выход/ШИМ).

**Примечания:**
- Разъем USB‑C чувствителен к ориентации. При проблемах переверните штекер.
- Если лента не стартует/не останавливается — нажмите **RESET** на плате.
- При работе по Wi‑Fi обеспечьте стабильность сети.
- Потеря яркости дисплея при подключении USB возможна и нормальна.
- Нет показаний сенсоров — перезапустите манипулятор и проверьте кабели.

---

## 12. Управление GPIO

```python
# Синхронная запись
manipulator.write_gpio(name, value, timeout_seconds=60.0, throw_error=True)
```

**Параметры:**  
`name` — строка; `value` — 0/1; `timeout_seconds`; `throw_error`.

**Пример:**
```python
gpio_name = "/dev/gpiochip4/e1_pin"

def set_led(on: bool):
    try:
        manipulator.write_gpio(gpio_name, 1 if on else 0, timeout_seconds=0.5, throw_error=False)
    except Exception as e:
        print(f"Ошибка управления GPIO: {e}")

set_led(True)
set_led(False)
```

---

## Примеры использования команд

SDK включает готовые примеры перемещений, работы с гриппером и др. Используйте для первичного ознакомления и проверки.

---

## Заключение

При проблемах используйте диагностические инструменты SDK и обращайтесь в поддержку с логами. Оборачивайте вызовы в `try/except` для корректной обработки ошибок.

---

Версия SDK: **0.6.7** © ПРОМОБОТ
