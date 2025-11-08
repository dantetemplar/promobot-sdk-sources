from sdk.manipulators.m13 import M13
import asyncio

if __name__ == "__main__":
    host: str = "192.168.88.72"
    client_id: str = "122"
    login: str = "13"
    password: str = "14"

    try:
        manipulator = M13(host, client_id, login, password)
        manipulator.connect()

        print("Подключение установлено")
        
        print("Координаты")
        print(manipulator.get_coordinates())
        
        print("Узлы")
        print(manipulator.get_joint_positions())
        
        print("Получено управление манипулятором")
        manipulator.get_manage()

        # Поворот
        manipulator.move_to_coordinates(0.25, 0.0, 0.15, 0, 0, 0, 1, 60, True)
        print("Манипулятор доехал в точку")
        manipulator.move_to_angles(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 60, True)
        print("Манипулятор доехал до углов")
        manipulator.nozzle_power(True, 60, True)
        print("Включили питание на стреле")
        manipulator.manage_gripper(10, 10, 60, True)
        print("Повернули гриппер")
        manipulator.manage_vacuum(10, True, 60, True)
        print("Включили вакуумный насос")

        manipulator.manage_vacuum(10, False, 60, True)
        print("Выключили вакуумный насос")
        manipulator.nozzle_power(False, 60, True)
        print("Выключили питание на стреле")
    except Exception as e:
        print("Возникла ошибка")
        print(e)