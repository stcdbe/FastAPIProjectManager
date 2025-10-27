from faststream.rabbit import QueueType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.types import AioPikaSendableMessage

from src.infra.worker.enum import RabbitExchangeName, RabbitQueueName


class RabbitMessageBroker:
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def start_broker(self) -> None:
        await self._broker.start()
        # declare dlq
        dlq = await self._broker.declare_queue(
            queue=RabbitQueue(
                name=RabbitQueueName.DLQ,
                queue_type=QueueType.QUORUM,
                durable=True,
                arguments={
                    "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
                    "x-delivery-limit": 5,
                },
            ),
        )
        # declare dlx
        dlx = await self._broker.declare_exchange(
            exchange=RabbitExchange(name=RabbitExchangeName.DLX, durable=True),
        )
        # bind dlq to dlx
        await dlq.bind(exchange=dlx, routing_key=dlq.name)

    async def stop_broker(self) -> None:
        await self._broker.stop()

    async def send_message(self, queue_name: RabbitQueueName, send_data: AioPikaSendableMessage) -> None:
        queue = RabbitQueue(
            name=queue_name,
            queue_type=QueueType.QUORUM,
            durable=True,
            arguments={
                "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
                "x-delivery-limit": 5,
                "x-dead-letter-exchange": RabbitExchangeName.DLX,
                "x-dead-letter-routing-key": RabbitQueueName.DLQ,
                "x-dead-letter-strategy": "at-least-once",
            },
        )

        await self._broker.publisher(queue=queue, content_type="application/json").publish(message=send_data)
