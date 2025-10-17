import atexit
from logging import Handler
from logging.handlers import QueueListener
from typing import Protocol, TypeVar

_T = TypeVar("_T")


class _QueueLike(Protocol[_T]):
    def get(self) -> _T: ...
    def put_nowait(self, item: _T, /) -> None: ...


class AutoStartQueueListener(QueueListener):
    def __init__(
        self,
        queue: _QueueLike[_T],
        *handlers: Handler,
        respect_handler_level: bool = False,
    ) -> None:
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        self.start()
        atexit.register(self.stop)
