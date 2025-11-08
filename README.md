# pm_python_sdk

## Подключение и установка
    from sdk.manipulators.medu import MEdu`
    
    manipulator = MEdu(host, client_id, login, password) # Создание экземпляра
    manipulator.connect() # Подключение к устройству

    # Чтобы определить host, выполните команду ip a на манипуляторе. client_id, login, password допускаются любые

## Команды
Перед выполнением команд требуется получить доступ к манипулятору:
`manipulator.get_control()`

### Перемещение в декартовых координатах
    manipulator.move_to_coordinates(
        MoveCoordinatesParamsPosition(0.3, 0, 0.2),
        MoveCoordinatesParamsOrientation(0, 0, 0, 1),
        0.2,
        0.2)

### Перемещение в углах
    manipulator.move_to_angles(0, 0, 1)

## Пример
    import asyncio

    from sdk.commands.move_coordinates_command import MoveCoordinatesParamsPosition, MoveCoordinatesParamsOrientation
    from sdk.manipulators.medu import MEdu

    host: str = 'localhost' # Чтобы определить host, выполните команду ip a на манипуляторе
    client_id: str = '12'
    login: str = '13'
    password: str = '14'
    
    manipulator = MEdu(host, client_id, login, password)
    
    try:
        manipulator.connect()
        print('Подключение установлено')
        coordinates = manipulator.get_cartesian_coordinates()
        print('Координаты')
        print(coordinates)
        joints = manipulator.get_joint_state()
        print('Узлы')
        print(joints)
        manipulator.get_control()
        print('Получено управление манипулятором')
        manipulator.move_to_coordinates(
            MoveCoordinatesParamsPosition(0.3, 0, 0.2),
            MoveCoordinatesParamsOrientation(0, 0, 0, 1),
            0.2,
            0.2)
        print('Манипулятор доехал в точку')
        manipulator.move_to_angles(0, 0, 1)
        print('Манипулятор доехал до углов')
        manipulator.nozzle_power(True)
        print('Включили питание на стреле')
        manipulator.manage_gripper(40, 40)
        print('Повернули гриппер')
        manipulator.manage_vacuum(-40, True)
        print('Включили вакуумный насос')
        await asyncio.sleep(5)
        manipulator.manage_vacuum(40, False)
        print('Выключили вакуумный насос')
        manipulator.nozzle_power(False)
        print('Выключили питание на стреле')
    except Exception as e:
        print('Возникла ошибка')
        print(e)