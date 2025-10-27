from src.domain.project.entities import ProjectReportData
from src.infra.worker.broker import RabbitMessageBroker
from src.infra.worker.enum import RabbitQueueName


class SendProjectReportUseCase:
    def __init__(self, message_broker: RabbitMessageBroker) -> None:
        self._message_broker = message_broker

    async def execute(self, send_data: ProjectReportData) -> None:
        await self._message_broker.send_message(RabbitQueueName.PROJECT_REPORT_NOTIFICATION, send_data)
