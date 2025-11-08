import sys, types
import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# -----------------------------------------------------------------------------
# Stub pydantic (минимум)
# -----------------------------------------------------------------------------
if "pydantic" not in sys.modules:
    pydantic_stub = types.ModuleType("pydantic")

    class _BaseModel:  # минимальная заглушка
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def _Field(*args, **kwargs):
        return None

    pydantic_stub.BaseModel = _BaseModel
    pydantic_stub.Field = _Field
    sys.modules["pydantic"] = pydantic_stub

# -----------------------------------------------------------------------------
# Stub paho-mqtt (клиент и сообщение)
# -----------------------------------------------------------------------------
if "paho" not in sys.modules:
    paho_stub = types.ModuleType("paho")
    mqtt_stub = types.ModuleType("paho.mqtt")
    client_stub = types.ModuleType("paho.mqtt.client")

    class _MQTTClient:
        def __init__(self, *a, **k):
            pass
        def connect(self, *a, **k):
            pass
        def publish(self, *a, **k):
            pass
        def subscribe(self, *a, **k):
            pass
        def loop_start(self):
            pass
        def loop_stop(self):
            pass

    class _MQTTMessage:
        topic: bytes
        payload: bytes

    client_stub.Client = _MQTTClient  # type: ignore
    client_stub.MQTTMessage = _MQTTMessage  # type: ignore

    mqtt_stub.client = client_stub  # type: ignore
    paho_stub.mqtt = mqtt_stub  # type: ignore

    sys.modules.update({
        "paho": paho_stub,
        "paho.mqtt": mqtt_stub,
        "paho.mqtt.client": client_stub,
    })

# -----------------------------------------------------------------------------
# Stub основных классов манипуляторов, чтобы старые тесты не ломались.
# -----------------------------------------------------------------------------
import types as _types

_stub_names = [
    "sdk.manipulators.manipulator",
    "sdk.manipulators.base",
    "sdk.manipulators.medu",
    "sdk.manipulators.m13",
]
_map_cls = {
    "sdk.manipulators.manipulator": "Manipulator",
    "sdk.manipulators.base": "BaseManipulator",
    "sdk.manipulators.medu": "MEdu",
    "sdk.manipulators.m13": "M13",
}

for _name in _stub_names:
    if _name not in sys.modules:
        mod = _types.ModuleType(_name)
        StubCls = type(_map_cls[_name], (), {"__init__": lambda self, *a, **k: None})
        setattr(mod, _map_cls[_name], StubCls)
        sys.modules[_name] = mod

# attachments
if "sdk.manipulators.attachments" not in sys.modules:
    att_stub = _types.ModuleType("sdk.manipulators.attachments")
    for cls in ["Attachment", "LaserAttachment", "GripperAttachment", "VacuumAttachment"]:
        setattr(att_stub, cls, object)
    sys.modules["sdk.manipulators.attachments"] = att_stub

import pytest

from sdk.manipulators.events import (
    on_command,
    on_command_result,
    on_management,
    on_coordinates,
    on_joint_states,
    EventMixin,
)
from sdk.utils.constants import (
    COMMAND_TOPIC,
    COMMAND_RESULT_TOPIC,
    MANAGEMENT_TOPIC,
    CARTESIAN_COORDINATES_TOPIC,
    JOINT_INFO_TOPIC,
)


class DummyMessageBus:
    """Мини-шина сообщений для тестов"""

    def __init__(self):
        self.subscriptions = {}

    def on_message(self, topic, handler):
        self.subscriptions.setdefault(topic, []).append(handler)

    def subscribe(self, topic):
        pass

    def unsubscribe(self, topic):
        pass

    def push(self, topic, payload):
        for sub, handlers in self.subscriptions.items():
            if sub == topic or sub == "#":
                for h in handlers:
                    if sub == "#":
                        h(topic, payload)
                    else:
                        h(payload)


class Dummy(EventMixin):
    def __init__(self):
        super().__init__()
        self.message_bus = DummyMessageBus()
        self.received = []

    @on_command
    def handle_command(self, payload):
        self.received.append(("cmd", payload))

    @on_coordinates
    def handle_coords(self, payload):
        self.received.append(("coords", payload))

    @on_command_result
    def handle_cmd_result(self, payload):
        self.received.append(("cmd_result", payload))

    @on_management
    def handle_mgmt(self, payload):
        self.received.append(("mgmt", payload))

    @on_joint_states
    def handle_joint(self, payload):
        self.received.append(("joint", payload))


@pytest.mark.parametrize(
    "prop, topic, payload",
    [
        ("on_command", COMMAND_TOPIC, {"k": 1}),
        ("on_command_result", COMMAND_RESULT_TOPIC, {"res": "ok"}),
        ("on_management", MANAGEMENT_TOPIC, {"state": "idle"}),
        ("on_coordinates", CARTESIAN_COORDINATES_TOPIC, {"x": 0.0}),
        ("on_joint_states", JOINT_INFO_TOPIC, {"j1": 0.1}),
    ],
)
def test_property_registration(prop, topic, payload):
    d = Dummy()
    called = []
    setattr(d, prop, lambda data: called.append(data))

    assert topic in d.message_bus.subscriptions
    d.message_bus.push(topic, payload)
    assert called == [payload]


def test_decorator_routing():
    d = Dummy()
    # активируем обёртки
    d.handle_command(None)
    d.handle_coords(None)
    d.handle_cmd_result(None)
    d.handle_mgmt(None)
    d.handle_joint(None)

    mapping = {
        COMMAND_TOPIC: "cmd",
        COMMAND_RESULT_TOPIC: "cmd_result",
        MANAGEMENT_TOPIC: "mgmt",
        CARTESIAN_COORDINATES_TOPIC: "coords",
        JOINT_INFO_TOPIC: "joint",
    }
    for t, lbl in mapping.items():
        p = {lbl: True}
        d.message_bus.push(t, p)
        assert (lbl, p) in d.received


def test_error_propagation():
    d = Dummy()
    d.on_command = lambda _: (_ for _ in ()).throw(RuntimeError("oops"))
    with pytest.raises(RuntimeError):
        d.message_bus.push(COMMAND_TOPIC, {}) 