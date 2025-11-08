from time import sleep
import asyncio
import json
from typing import Dict, Optional, Callable, Any

from sdk.commands.gripper_control_command import GripperControlCommand
from sdk.commands.nozzle_power_command import NozzlePowerCommand
from sdk.commands.vacuum_control_command import VacuumControlCommand
from sdk.commands.move_angles_command import MoveAnglesCommand, MoveAnglesCommandParamsAngleInfo
from sdk.manipulators.manipulator import Manipulator
from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC, JOINT_INFO_TOPIC
from sdk.manipulators.manipulator_connection import ManipulatorConnection
from sdk.commands.abstracts.sdk_command import NoWaitCommand
from sdk.commands.manipulator_commands import GetI2C
from sdk.manipulators.extern_devices.mgbot.mgbot_conveyer import MGbotConveyer

class MEdu (Manipulator):
    message_bus: ManipulatorConnection
    joint_state_callback: Optional[Callable]

    def __init__(self, host: str, client_id: str, login: str, password: str):
        super(MEdu, self).__init__(host, client_id, login, password)
        self.joint_state_callback = None
        self.mgbot_conveyer = MGbotConveyer(self.message_bus, self._run_async, self)

    def _cleanup_finished_commands(self):
        finished_ids = []
        for cmd_id, command in self.active_commands.items():
            if hasattr(command, 'promise') and not command.promise.is_active:
                finished_ids.append(cmd_id)
        
        for cmd_id in finished_ids:
            del self.active_commands[cmd_id]

    def move_to_angles(self, povorot_osnovaniya: float, privod_plecha: float, privod_strely: float, 
                     v_osnovaniya: float = 0.0, v_plecha: float = 0.0, v_strely: float = 0.0,
                     velocity_factor: float = 0.1, acceleration_factor: float = 0.1,
                     timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """
        Осуществить поворот на заданный угол
        :param povorot_osnovaniya: Целевой угол поворота основания
        :param privod_plecha: Целевой угол плеча
        :param privod_strely: Целевой угол стрелы
        :param v_osnovaniya: Скорость поворота основания в рад/с
        :param v_plecha: Скорость движения плеча в рад/с
        :param v_strely: Скорость движения стрелы в рад/с
        :param velocity_factor: % от максимальной скорости (0.0 - 1.0)
        :param acceleration_factor: % от максимального ускорения (0.0 - 1.0)
        :param timeout_seconds: Timeout операции (по умолчанию 60 секунд)
        :param throw_error: Флаг выбрасывания исключения при ошибке
        :return:
        """
        angles = [
            MoveAnglesCommandParamsAngleInfo("povorot_osnovaniya", povorot_osnovaniya, v_osnovaniya),
            MoveAnglesCommandParamsAngleInfo("privod_plecha", privod_plecha, v_plecha),
            MoveAnglesCommandParamsAngleInfo("privod_strely", privod_strely, v_strely)
        ]
        
        self.move_angles_command = MoveAnglesCommand(
            self.message_bus.publish, 
            angles, 
            timeout_seconds, 
            throw_error,
            velocity_factor,
            acceleration_factor,
            self.message_bus
        )
        
        self.active_commands[self.move_angles_command.command_id] = self.move_angles_command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.move_angles_command.make_command_action()  # Отправляем команду
        
        try:
            result = self.move_angles_command.result()
        finally:
            # Команда будет удалена автоматически после  ответа
            self.move_angles_command = None

    async def move_to_angles_async(
        self,
        povorot_osnovaniya: float,
        privod_plecha: float,
        privod_strely: float,
        v_osnovaniya: float = 0.0,
        v_plecha: float = 0.0,
        v_strely: float = 0.0,
        velocity_factor: float = 0.1,
        acceleration_factor: float = 0.1,
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
    ) -> None:
        """
        Асинхронное перемещение по углам с поддержкой параллельного выполнения
        """
        angles = [
            MoveAnglesCommandParamsAngleInfo("povorot_osnovaniya", povorot_osnovaniya, v_osnovaniya),
            MoveAnglesCommandParamsAngleInfo("privod_plecha", privod_plecha, v_plecha),
            MoveAnglesCommandParamsAngleInfo("privod_strely", privod_strely, v_strely)
        ]
        
        command = MoveAnglesCommand(
            self.message_bus.publish, 
            angles, 
            timeout_seconds, 
            throw_error,
            velocity_factor,
            acceleration_factor,
            self.message_bus
        )
        
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        
        command.make_command_action()
        
        await command.promise.async_result()

    async def move_to_angles_async_await(
        self,
        povorot_osnovaniya: float,
        privod_plecha: float,
        privod_strely: float,
        v_osnovaniya: float = 0.0,
        v_plecha: float = 0.0,
        v_strely: float = 0.0,
        velocity_factor: float = 0.1,
        acceleration_factor: float = 0.1,
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
    ) -> None:
        await self.move_to_angles_async(
            povorot_osnovaniya,
            privod_plecha,
            privod_strely,
            v_osnovaniya,
            v_plecha,
            v_strely,
            velocity_factor,
            acceleration_factor,
            timeout_seconds,
            throw_error,
        )

    def move_to_angles_no_wait(self, povorot_osnovaniya: float, privod_plecha: float, privod_strely: float,
                             v_osnovaniya: float = 0.0, v_plecha: float = 0.0, v_strely: float = 0.0,
                             velocity_factor: float = 0.1, acceleration_factor: float = 0.1) -> None:
        """
        Осуществить поворот на заданный угол без ожидания результата
        :param povorot_osnovaniya: Целевой угол поворота основания
        :param privod_plecha: Целевой угол плеча
        :param privod_strely: Целевой угол стрелы
        :param v_osnovaniya: Скорость поворота основания в рад/с
        :param v_plecha: Скорость движения плеча в рад/с
        :param v_strely: Скорость движения стрелы в рад/с
        :param velocity_factor: % от максимальной скорости (0.0 - 1.0)
        :param acceleration_factor: % от максимального ускорения (0.0 - 1.0)
        """
        
        data = {
            "positions": {
                "povorot_osnovaniya": povorot_osnovaniya,
                "privod_plecha": privod_plecha,
                "privod_strely": privod_strely
            },
            "velocities": {
                "povorot_osnovaniya": v_osnovaniya,
                "privod_plecha": v_plecha,
                "privod_strely": v_strely
            },
            "velocity_factor": velocity_factor,
            "acceleration_factor": acceleration_factor
        }
        
        command = NoWaitCommand(self.message_bus.publish, "move_joints", data, message_bus=self.message_bus)
        self.active_commands[command.command_id] = command
        command.make_command_action()

    def nozzle_power(self, power: bool, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """
        Подача питания на разъемы на стреле
        :param power: Признак наличия питания
        :param timeout_seconds: Timeout операции (по умолчанию 60 секунд)
        :param throw_error: Флаг выбрасывания исключения при ошибке
        """
        command = NozzlePowerCommand(self.message_bus.publish, power, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()  # Отправляем команду
        try:
            result = command.result()
            return result
        finally:
            pass

    async def nozzle_power_async(
        self,
        power: bool,
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
    ) -> None:
        """
        Асинхронная подача питания на разъемы на стреле с поддержкой параллелизма
        """
        command = NozzlePowerCommand(self.message_bus.publish, power, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()
        try:
            await command.promise.async_result()
        finally:
            # Команда будет удалена автоматически после обработки ответа
            pass

    def nozzle_power_no_wait(self, power: bool) -> None:
        """
        Подача питания на разъемы на стреле без ожидания результата
        :param power: Признак наличия питания
        """

        command = NoWaitCommand(self.message_bus.publish, "nozzle_power", {"power_supply": power}, message_bus=self.message_bus)
        self.active_commands[command.command_id] = command
        command.make_command_action()

    def manage_gripper(self, rotation: int = None, gripper: int = None, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """
        Управление гриппером (доступно только при поданном питании - nozzle_power)
        :param rotation: Угол поворота насадки (градусы)
        :param gripper: Угол сжатия гриппера (градусы)
        :param timeout_seconds: Timeout операции (по умолчанию 60 секунд)
        :param throw_error: Флаг выбрасывания исключения при ошибке
        """
        if rotation == None and gripper == None:
            raise ValueError("At least one of rotation or gripper must be provided")
        command = GripperControlCommand(self.message_bus.publish, rotation, gripper, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()  # Отправляем команду
        try:
            result = command.result()
            return result
        finally:
            pass

    async def manage_gripper_async(
        self,
        rotation: int = None,
        gripper: int = None,
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
    ) -> None:
        """
        Асинхронное управление гриппером с поддержкой параллелизма
        """
        if rotation == None and gripper == None:
            raise ValueError("At least one of rotation or gripper must be provided")
        command = GripperControlCommand(self.message_bus.publish, rotation, gripper, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()
        try:
            await command.promise.async_result()
        finally:
            pass

    def manage_gripper_no_wait(self, rotation: int = None, gripper: int = None) -> None:
        """
        Управление гриппером без ожидания результата (доступно только при поданном питании - nozzle_power)
        :param rotation: Угол поворота насадки (градусы)
        :param gripper: Угол сжатия гриппера (градусы)
        """
        if rotation == None and gripper == None:
            raise ValueError("At least one of rotation or gripper must be provided")
        command = NoWaitCommand(self.message_bus.publish, "gripper_control", {"rotation": rotation, "gripper": gripper}, message_bus=self.message_bus)
        self.active_commands[command.command_id] = command
        command.make_command_action()

    def manage_vacuum(self, rotation: int = None, power_supply: bool = None, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        """
        Управление вакуумным насосом (доступно только при поданном питании - nozzle_power)
        :param rotation: Угол поворота насадки (градусы)
        :param power_supply: Признак включения вакуумного насоса
        :param timeout_seconds: Timeout операции (по умолчанию 60 секунд)
        :param throw_error: Флаг выбрасывания исключения при ошибке
        """
        if rotation == None and power_supply == None:
            raise ValueError("At least one of rotation or power_supply must be provided")
        command = VacuumControlCommand(self.message_bus.publish, rotation, power_supply, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()  # Отправляем команду
        try:
            result = command.result()
            return result
        finally:
            pass

    async def manage_vacuum_async(
        self,
        rotation: int = None,
        power_supply: bool = None,
        timeout_seconds: float = 60.0,
        throw_error: bool = True,
    ) -> None:
        if rotation == None and power_supply == None:
            raise ValueError("At least one of rotation or power_supply must be provided")
        command = VacuumControlCommand(self.message_bus.publish, rotation, power_supply, timeout_seconds, throw_error, self.message_bus)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()
        try:
            await command.promise.async_result()
        finally:
            pass

    def manage_vacuum_no_wait(self, rotation: int, power_supply: bool) -> None:
        """
        Управление вакуумным насосом без ожидания результата (доступно только при поданном питании - nozzle_power)
        :param rotation: Угол поворота насадки (градусы)
        :param power_supply: Признак включения вакуумного насоса
        """
        if rotation == None and power_supply == None:
            raise ValueError("At least one of rotation or power_supply must be provided")
        data = {}
        if rotation is not None:
            data["rotation"] = rotation
        if power_supply is not None:
            data["power_supply"] = power_supply
        command = NoWaitCommand(self.message_bus.publish, "vacuum_control", data, message_bus=self.message_bus)
        self.active_commands[command.command_id] = command
        command.make_command_action()

    def stream_joint_angles(self, povorot_osnovaniya: float, privod_plecha: float, privod_strely: float,
                           v_osnovaniya: float = 0.0, v_plecha: float = 0.0, v_strely: float = 0.0) -> None:
        """
        Стриминг углов для MEdu манипулятора
        :param povorot_osnovaniya: Угол поворота основания в радианах
        :param privod_plecha: Угол плеча в радианах
        :param privod_strely: Угол стрелы в радианах
        :param v_osnovaniya: Скорость поворота основания в рад/с
        :param v_plecha: Скорость движения плеча в рад/с
        :param v_strely: Скорость движения стрелы в рад/с
        """
        positions = {
            "povorot_osnovaniya": povorot_osnovaniya,
            "privod_plecha": privod_plecha,
            "privod_strely": privod_strely
        }

        velocities = {
            "povorot_osnovaniya": v_osnovaniya,
            "privod_plecha": v_plecha,
            "privod_strely": v_strely
        }

        self.stream_joint_positions(positions, velocities)

    async def stream_joint_angles_async(self, povorot_osnovaniya: float, privod_plecha: float, privod_strely: float,
                                      v_osnovaniya: float = 0.0, v_plecha: float = 0.0, v_strely: float = 0.0) -> None:
        """
        Асинхронный стриминг углов для MEdu манипулятора
        :param povorot_osnovaniya: Угол поворота основания в радианах
        :param privod_plecha: Угол плеча в радианах
        :param privod_strely: Угол стрелы в радианах
        :param v_osnovaniya: Скорость поворота основания в рад/с
        :param v_plecha: Скорость движения плеча в рад/с
        :param v_strely: Скорость движения стрелы в рад/с
        """
        positions = {
            "povorot_osnovaniya": povorot_osnovaniya,
            "privod_plecha": privod_plecha,
            "privod_strely": privod_strely
        }
        
        velocities = {
            "povorot_osnovaniya": v_osnovaniya,
            "privod_plecha": v_plecha,
            "privod_strely": v_strely
        }
        
        await self.stream_joint_positions_async(positions, velocities)

    def subscribe_to_joint_state(self, callback: callable) -> None:
        """
        Подписаться на обновления состояния узлов манипулятора
        :param callback: Функция обратного вызова, принимающая параметр с данными состояния узлов
        """
        self.joint_state_callback = callback
        self.message_bus.subscribe(JOINT_INFO_TOPIC)
    
    def unsubscribe_from_joint_state(self) -> None:
        """
        Отписаться от обновлений состояния узлов манипулятора
        """
        self.joint_state_callback = None
        self.message_bus.unsubscribe(JOINT_INFO_TOPIC)
    
    def process_message(self, topic: str, payload: str) -> None:
        self._cleanup_finished_commands()
        if topic == "/command_result":
            import json
            try:
                data = json.loads(payload)
                command_id = data.get("id")
                print(f"[MEdu] Обрабатываем ответ для command_id={command_id}")
                print(f"[MEdu] active_commands keys: {list(self.active_commands.keys())}")
                if command_id in self.active_commands:
                    print(f"[MEdu] Найдена команда {command_id}, передаем в process_message")
                    self.active_commands[command_id].process_message(topic, payload)
                else:
                    print(f"[MEdu] Команда {command_id} НЕ найдена в active_commands!")
            except Exception as e:
                print(f"[MEdu] ОШИБКА при обработке /command_result: {e}")
                import traceback
                traceback.print_exc()
        if topic == JOINT_INFO_TOPIC and self.joint_state_callback is not None:
            try:
                data = json.loads(payload)
                self.joint_state_callback(data)
            except Exception as e:
                print(f"[MEdu] ОШИБКА при обработке joint state: {e}")
        super().process_message(topic, payload)

    def get_i2c_value(self, name: str, timeout_seconds: float = 60.0, throw_error: bool = True) -> Optional[float]:
        self.specific_command = GetI2C(self.message_bus.publish, name, timeout_seconds, throw_error)
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command.make_command_action()
        result: dict[str, Any] = self.specific_command.result()
        self.specific_command = None
        return result.get('data', {}).get('value', None)
