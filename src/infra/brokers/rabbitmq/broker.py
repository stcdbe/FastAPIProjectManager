from logging import getLogger

from faststream.rabbit import QueueType, RabbitBroker, RabbitExchange, RabbitQueue

from src.infra.brokers.base import AbstractMessageBroker, DataclassInstance
from src.infra.brokers.enums import ExchangeName, QueueName
from src.infra.brokers.rabbitmq.worker_routes import worker_router


class RabbitMQMessageBroker(AbstractMessageBroker):
    __slots__ = ("_broker",)

    _broker: RabbitBroker

    def __init__(self, broker_url: str) -> None:
        self._broker = RabbitBroker(
            url=broker_url,
            logger=getLogger(),
        )
        self._broker.include_router(worker_router)

    async def start_broker(self) -> None:
        await self._broker.start()
        # declare dlq
        dlq = await self._broker.declare_queue(
            queue=RabbitQueue(
                name=QueueName.DLQ,
                queue_type=QueueType.QUORUM,
                durable=True,
                arguments={
                    "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
                    "x-delivery-limit": 5,
                },
            ),
        )
        # declare dlx
        dlx = await self._broker.declare_exchange(exchange=RabbitExchange(name=ExchangeName.DLX, durable=True))
        # bind dlq to dlx
        await dlq.bind(exchange=dlx, routing_key=dlq.name)

    async def stop_broker(self) -> None:
        await self._broker.stop()

    async def send_message(self, queue_name: QueueName, send_data: DataclassInstance) -> None:
        queue = RabbitQueue(
            name=queue_name,
            queue_type=QueueType.QUORUM,
            durable=True,
            arguments={
                "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
                "x-delivery-limit": 5,
                "x-dead-letter-exchange": ExchangeName.DLX,
                "x-dead-letter-routing-key": QueueName.DLQ,
                "x-dead-letter-strategy": "at-least-once",
            },
        )

        await self._broker.publisher(queue=queue, content_type="application/json").publish(message=send_data)
