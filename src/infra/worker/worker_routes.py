from typing import Any

from faststream import Depends, Logger
from faststream.rabbit import QueueType, RabbitQueue, RabbitRouter
from punq import Container

from src.domain.project.entities import ProjectReportData
from src.domain.project_task_aggregation.flows.send_project_report_notification import SendProjectReportNotificationFlow
from src.infra.worker.enums import RabbitMQExchangeName, RabbitMQQueueName
from src.logic.worker_di_container import get_worker_di_container

worker_router = RabbitRouter()


@worker_router.subscriber(
    queue=RabbitQueue(
        name=RabbitMQQueueName.DEAD_LETTER,
        queue_type=QueueType.QUORUM,
        durable=True,
        arguments={
            "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
            "x-delivery-limit": 5,
        },
    ),
)
async def dlq_handler(body: dict[str, Any], logger: Logger) -> None:
    logger.error("dlq payload: %s", body)
    # error handling business logic flow


@worker_router.subscriber(
    queue=RabbitQueue(
        name=RabbitMQQueueName.SEND_PROJECT_REPORT_NOTIFICATION,
        queue_type=QueueType.QUORUM,
        durable=True,
        arguments={
            "x-message-ttl": 60 * 60 * 1000,  # 1 hour in ms
            "x-delivery-limit": 5,
            "x-dead-letter-exchange": RabbitMQExchangeName.DEAD_LETTER,
            "x-dead-letter-routing-key": RabbitMQQueueName.DEAD_LETTER,
            "x-dead-letter-strategy": "at-least-once",
        },
    ),
)
async def send_project_report_notification(
    body: ProjectReportData,
    logger: Logger,
    container: Container = Depends(get_worker_di_container),  # noqa: B008
) -> None:
    logger.info("project report notification payload: %s", body)
    flow: SendProjectReportNotificationFlow = container.resolve(SendProjectReportNotificationFlow)  # type: ignore
    await flow.execute(body)
