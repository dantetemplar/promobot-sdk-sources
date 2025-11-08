from abc import abstractmethod
from typing import Callable, Any

from sdk.promise import Promise

class AsyncOperation:
    def __init__(self, send_command: Callable[[str, dict], None], timeout_seconds: float = 60.0, throw_error: bool = True, feedback: bool = False):
        self.promise = Promise(timeout_seconds, throw_error)
        self.send_command = send_command
        self.feedback = feedback

    def result(self) -> None:
        return self.promise.result()

    async def async_result(self) -> Any:
        return await self.promise.async_result()

    @property
    def is_active(self) -> bool:
        return self.promise.is_active

    @abstractmethod
    def make_command_action(self) -> None:
        pass

    @abstractmethod
    def process_message(self, topic: str, message: str) -> None:
        pass

    def __await__(self):
        return self.promise.__await__()