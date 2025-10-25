from typing import Any

from faststream import Logger
from faststream.rabbit import QueueType, RabbitQueue, RabbitRouter

from src.domain.project.entities import ProjectReportData
from src.domain.project_task_aggregation.flows.send_project_report_notification import SendProjectReportNotificationFlow

background_router = RabbitRouter()


@background_router.subscriber(
    queue=RabbitQueue(
        name="dlq",
        queue_type=QueueType.QUORUM,
        durable=True,
        arguments={
            "x-message-ttl": 12 * 60 * 60 * 1000,
            "x-delivery-limit": 5,
        },
    ),
)
async def dlq_handler(body: dict[str, Any], logger: Logger) -> None:
    logger.error("dlq payload: %s", body)


@background_router.subscriber(
    queue=RabbitQueue(
        name="project_notifications",
        queue_type=QueueType.QUORUM,
        durable=True,
        arguments={
            "x-message-ttl": 12 * 60 * 60 * 1000,
            "x-delivery-limit": 5,
        },
    ),
)
async def send_project_report_notification(body: ProjectReportData, logger: Logger) -> None:
    logger.info("wh payload: %s", body)
    flow = SendProjectReportNotificationFlow()
    await flow.execute(body)
