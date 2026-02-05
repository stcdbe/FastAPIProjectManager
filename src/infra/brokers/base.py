from abc import ABC, abstractmethod
from dataclasses import Field
from typing import Any, ClassVar, Protocol

from src.infra.brokers.enums import QueueName


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class AbstractMessageBroker(ABC):
    @abstractmethod
    async def start_broker(self) -> None: ...

    @abstractmethod
    async def stop_broker(self) -> None: ...

    @abstractmethod
    async def send_message(self, queue_name: QueueName, send_data: DataclassInstance) -> None: ...
