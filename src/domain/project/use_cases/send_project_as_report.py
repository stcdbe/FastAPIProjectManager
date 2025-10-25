from faststream.rabbit import QueueType, RabbitQueue

from src.domain.project.entities import ProjectReportData
from src.infra.broker.rabbitmq_broker import broker


class SendProjectAsReportUseCase:
    async def execute(self, send_data: ProjectReportData) -> None:
        await broker.publisher(
            queue=RabbitQueue(
                name="project_notifications",
                queue_type=QueueType.QUORUM,
                durable=True,
                arguments={
                    "x-message-ttl": 12 * 60 * 60 * 1000,
                    "x-delivery-limit": 5,
                    "x-dead-letter-exchange": "dlx",
                    "x-dead-letter-routing-key": "dlq",
                    "x-dead-letter-strategy": "at-least-once",
                },
            ),
            content_type="application/json",
        ).publish(message=send_data)
