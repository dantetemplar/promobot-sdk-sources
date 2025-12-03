from sdk.manipulators.manipulator import Manipulator
from typing import Dict, Optional, Any
from sdk.utils.constants import JOINT_INFO_TOPIC
import json

from sdk.commands.palletizing_movement import PaletizingMovement
from sdk.commands.move_angles_command import MoveAnglesCommandParamsAngleInfo
from sdk.commands.data import Pose, Orientation
from sdk.commands.gpio_mask import SetGpioMask, GetGpioMask
from sdk.commands.manipulator_commands import GPIOConfigurePin
from sdk.utils.constants import COMMAND_TOPIC, COMMAND_RESULT_TOPIC, COMMAND_FEEDBACK_TOPIC


class M13 (Manipulator):
    def __init__(self, host: str, client_id: str, login: str, password: str):
        super(M13, self).__init__(host, client_id, login, password)
        self.joint_state_callback = None

    def move_to_angles(self, sp1: float, sp2: float, sp3: float, sp4: float, sp5: float, sp6: float,
                       sp1_v: float = 0.0, sp2_v: float = 0.0, sp3_v: float = 0.0,
                       sp4_v: float = 0.0, sp5_v: float = 0.0, sp6_v: float = 0.0,
                       velocity_factor: float = 0.1, acceleration_factor: float = 0.1,
                       timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        angles = [
            MoveAnglesCommandParamsAngleInfo('shoulder_pan_joint', sp1, sp1_v),
            MoveAnglesCommandParamsAngleInfo('shoulder_lift_joint', sp2, sp2_v),
            MoveAnglesCommandParamsAngleInfo('elbow_joint', sp3, sp3_v),
            MoveAnglesCommandParamsAngleInfo('wrist_1_joint', sp4, sp4_v),
            MoveAnglesCommandParamsAngleInfo('wrist_2_joint', sp5, sp5_v),
            MoveAnglesCommandParamsAngleInfo('wrist_3_joint', sp6, sp6_v)
        ]
        self._run_move_to_angles_command(angles, timeout_seconds, throw_error, velocity_factor, acceleration_factor)

    async def move_to_angles_async(self, sp1: float, sp2: float, sp3: float, sp4: float, sp5: float, sp6: float,
                                   sp1_v: float = 0.0, sp2_v: float = 0.0, sp3_v: float = 0.0,
                                   sp4_v: float = 0.0, sp5_v: float = 0.0, sp6_v: float = 0.0,
                                   velocity_factor: float = 0.1, acceleration_factor: float = 0.1,
                                   timeout_seconds: float = 60.0, throw_error: bool = True) -> None:

        await self._run_async(
            self.move_to_angles,
            sp1, sp2, sp3, sp4, sp5, sp6,
            sp1_v, sp2_v, sp3_v, sp4_v, sp5_v, sp6_v,
            velocity_factor, acceleration_factor,
            timeout_seconds,
            throw_error,
        )

    def move_to_angles_no_wait(self, sp1: float, sp2: float, sp3: float, sp4: float, sp5: float, sp6: float,
                       sp1_v: float = 0.0, sp2_v: float = 0.0, sp3_v: float = 0.0,
                       sp4_v: float = 0.0, sp5_v: float = 0.0, sp6_v: float = 0.0,
                       velocity_factor: float = 0.1, acceleration_factor: float = 0.1) -> None:
        """
        Переместить манипулятор в заданные углы без ожидания результата выполнения
        :param sp1: Угол для shoulder_pan_joint в радианах
        :param sp2: Угол для shoulder_lift_joint в радианах
        :param sp3: Угол для elbow_joint в радианах
        :param sp4: Угол для wrist_1_joint в радианах
        :param sp5: Угол для wrist_2_joint в радианах
        :param sp6: Угол для wrist_3_joint в радианах
        """
        angles = [
            MoveAnglesCommandParamsAngleInfo('shoulder_pan_joint', sp1, sp1_v),
            MoveAnglesCommandParamsAngleInfo('shoulder_lift_joint', sp2, sp2_v),
            MoveAnglesCommandParamsAngleInfo('elbow_joint', sp3, sp3_v),
            MoveAnglesCommandParamsAngleInfo('wrist_1_joint', sp4, sp4_v),
            MoveAnglesCommandParamsAngleInfo('wrist_2_joint', sp5, sp5_v),
            MoveAnglesCommandParamsAngleInfo('wrist_3_joint', sp6, sp6_v)
        ]
        self._run_move_to_angles_command_no_wait(angles, velocity_factor, acceleration_factor)

    def stream_joint_angles(self, sp1: float, sp2: float, sp3: float, sp4: float, sp5: float, sp6: float, 
                           v1: float = 0.0, v2: float = 0.0, v3: float = 0.0, v4: float = 0.0, v5: float = 0.0, v6: float = 0.0) -> None:
        """
        Стриминг углов для M13 манипулятора
        :param sp1: Угол для shoulder_pan_joint в радианах
        :param sp2: Угол для shoulder_lift_joint в радианах
        :param sp3: Угол для elbow_joint в радианах
        :param sp4: Угол для wrist_1_joint в радианах
        :param sp5: Угол для wrist_2_joint в радианах
        :param sp6: Угол для wrist_3_joint в радианах
        :param v1: Скорость для shoulder_pan_joint в рад/с
        :param v2: Скорость для shoulder_lift_joint в рад/с
        :param v3: Скорость для elbow_joint в рад/с
        :param v4: Скорость для wrist_1_joint в рад/с
        :param v5: Скорость для wrist_2_joint в рад/с
        :param v6: Скорость для wrist_3_joint в рад/с
        """
        positions = {
            "shoulder_pan_joint": sp1,
            "shoulder_lift_joint": sp2,
            "elbow_joint": sp3,
            "wrist_1_joint": sp4,
            "wrist_2_joint": sp5,
            "wrist_3_joint": sp6
        }
        
        velocities = {
            "shoulder_pan_joint": v1,
            "shoulder_lift_joint": v2,
            "elbow_joint": v3,
            "wrist_1_joint": v4,
            "wrist_2_joint": v5,
            "wrist_3_joint": v6
        }
        
        self.stream_joint_positions(positions, velocities)

    async def stream_joint_angles_async(self, sp1: float, sp2: float, sp3: float, sp4: float, sp5: float, sp6: float, 
                                      v1: float = 0.0, v2: float = 0.0, v3: float = 0.0, v4: float = 0.0, v5: float = 0.0, v6: float = 0.0) -> None:
        """
        Асинхронный стриминг углов для M13 манипулятора
        :param sp1: Угол для shoulder_pan_joint в радианах
        :param sp2: Угол для shoulder_lift_joint в радианах
        :param sp3: Угол для elbow_joint в радианах
        :param sp4: Угол для wrist_1_joint в радианах
        :param sp5: Угол для wrist_2_joint в радианах
        :param sp6: Угол для wrist_3_joint в радианах
        :param v1: Скорость для shoulder_pan_joint в рад/с
        :param v2: Скорость для shoulder_lift_joint в рад/с
        :param v3: Скорость для elbow_joint в рад/с
        :param v4: Скорость для wrist_1_joint в рад/с
        :param v5: Скорость для wrist_2_joint в рад/с
        :param v6: Скорость для wrist_3_joint в рад/с
        """
        positions = {
            "shoulder_pan_joint": sp1,
            "shoulder_lift_joint": sp2,
            "elbow_joint": sp3,
            "wrist_1_joint": sp4,
            "wrist_2_joint": sp5,
            "wrist_3_joint": sp6
        }
        
        velocities = {
            "shoulder_pan_joint": v1,
            "shoulder_lift_joint": v2,
            "elbow_joint": v3,
            "wrist_1_joint": v4,
            "wrist_2_joint": v5,
            "wrist_3_joint": v6
        }
        
        await self.stream_joint_positions_async(positions, velocities)
        
    def paletizing_movement_async(self,
                                  target_point: Pose,
                                  hold_orientation: Orientation = Orientation(),
                                  use_orientation: bool = False,
                                  step: float = 0.05,
                                  count_point: int = 50,
                                  max_velocity_scaling_factor: float = 0.1,
                                  max_acceleration_scaling_factor: float = 0.1,
                                  timeout_seconds: float = 60.0,
                                  throw_error: bool = True,
                                  enable_feedback: bool = False) -> PaletizingMovement:
        self.specific_command = PaletizingMovement(target_point,
                                     hold_orientation,
                                     use_orientation,
                                     step,
                                     count_point,
                                     max_velocity_scaling_factor,
                                     max_acceleration_scaling_factor,
                                     self.message_bus.send_message,
                                     timeout_seconds,
                                     throw_error,
                                     enable_feedback)
        self.active_commands[self.specific_command.command_id] = self.specific_command
        if enable_feedback:
            self.specific_command.promise.add_feedback_callback(self._on_run_feedback)
        self.message_bus.subscribe(COMMAND_FEEDBACK_TOPIC)
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command.make_command_action()
        return self.specific_command

    async def paletizing_movement_async_await(self,
                                              target_point: Pose,
                                              hold_orientation: Orientation = Orientation(),
                                              use_orientation: bool = False,
                                              step: float = 0.05,
                                              count_point: int = 50,
                                              max_velocity_scaling_factor: float = 0.1,
                                              max_acceleration_scaling_factor: float = 0.1,
                                              timeout_seconds: float = 60.0,
                                              throw_error: bool = True) -> None:
        command = PaletizingMovement(target_point,
                                     hold_orientation,
                                     use_orientation,
                                     step,
                                     count_point,
                                     max_velocity_scaling_factor,
                                     max_acceleration_scaling_factor,
                                     self.message_bus.send_message,
                                     timeout_seconds,
                                     throw_error)
        self.active_commands[command.command_id] = command
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        command.make_command_action()
        try:
            result = self.specific_command.result()
            return result
        finally:
            self.specific_command = None
            pass
 
    def paletizing_movement(self,
                            target_point: Pose,
                            hold_orientation: Orientation = Orientation(),
                            use_orientation: bool = False,
                            step: float = 0.05,
                            count_point: int = 50,
                            max_velocity_scaling_factor: float = 0.1,
                            max_acceleration_scaling_factor: float = 0.1,
                            timeout_seconds: float = 60.0,
                            throw_error: bool = True) -> None:
        command = self.paletizing_movement_async(target_point,
                                                 hold_orientation,
                                                 use_orientation,
                                                 step,
                                                 count_point,
                                                 max_velocity_scaling_factor,
                                                 max_acceleration_scaling_factor,
                                                 timeout_seconds,
                                                 throw_error)
        command.result()
        self.specific_command = None

    def gpio_configure_pin(self, name: str, value: bool, timeout_seconds: float = 60.0, throw_error: bool = True) -> bool:
        self.specific_command = GPIOConfigurePin(self.message_bus.publish, name, value, timeout_seconds, throw_error)
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command.make_command_action()
        result: dict[str, Any] = self.specific_command.result()
        self.specific_command = None
        return result.get('result', False)

    def set_gpio_on_mask(self, name: str, value_mask: str, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command = SetGpioMask(self.message_bus.send_message, name, value_mask, timeout_seconds, throw_error)
        self.specific_command.result()

    async def set_gpio_on_mask_async(self, name: str, value_mask: str, timeout_seconds: float = 60.0, throw_error: bool = True) -> None:
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.message_bus.subscribe(COMMAND_RESULT_TOPIC)
        self.specific_command = SetGpioMask(self.message_bus.send_message, name, value_mask, timeout_seconds, throw_error)
        await self.specific_command.async_result()

    def get_gpio_mask(self, name: str, timeout_seconds: float = 60.0, throw_error: bool = True) -> Dict[str, Any]:
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.specific_command = GetGpioMask(self.message_bus.send_message, name, timeout_seconds, throw_error)
        return self.info.get_result_command(self.specific_command)['data']

    async def get_gpio_mask_async(self, name: str, timeout_seconds: float = 60.0, throw_error: bool = True) -> Dict[str, Any]:
        self.message_bus.subscribe(COMMAND_TOPIC)
        self.specific_command = GetGpioMask(self.message_bus.send_message, name, timeout_seconds, throw_error)
        return (await self.info.get_result_command_async(self.specific_command))['data']

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
        """
        Обработка входящих сообщений
        :param topic: Топик сообщения
        :param payload: Содержимое сообщения
        """
        super().process_message(topic, payload)
        
        # Если есть подписка на состояние узлов и пришло соответствующее сообщение
        if self.joint_state_callback is not None and topic == JOINT_INFO_TOPIC:
            try:
                if isinstance(payload, str):
                    joint_data = json.loads(payload)
                else:
                    joint_data = payload
                # Вызов функции обратного вызова с данными
                self.joint_state_callback(joint_data)
            except Exception as e:
                print(f"Ошибка обработки данных состояния узлов: {str(e)}")
