from logging import getLogger

from src.infra.brokers.base import AbstractMessageBroker, DataclassInstance
from src.infra.brokers.enums import QueueName

_logger = getLogger()


class ConsoleMessageBroker(AbstractMessageBroker):
    __slots__ = ()

    async def start_broker(self) -> None:
        _logger.info("Starting broker")

    async def stop_broker(self) -> None:
        _logger.info("Stopping broker")

    async def send_message(self, queue_name: QueueName, send_data: DataclassInstance) -> None:
        _logger.info("Sending message data %s to queue %r", send_data, queue_name)
