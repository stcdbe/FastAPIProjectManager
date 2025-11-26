import atexit
from logging import Handler
from logging.handlers import QueueListener
from typing import Any, Protocol


class _QueueLike[T](Protocol):
    def get(self) -> T: ...
    def put_nowait(self, item: T, /) -> None: ...


class AutoStartQueueListener(QueueListener):
    def __init__(
        self,
        queue: _QueueLike[Any],
        *handlers: Handler,
        respect_handler_level: bool = False,
    ) -> None:
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        self.start()
        atexit.register(self.stop)
