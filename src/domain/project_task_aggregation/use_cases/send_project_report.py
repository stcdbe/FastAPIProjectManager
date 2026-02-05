from src.domain.project.entities import ProjectReportData
from src.infra.brokers.base import AbstractMessageBroker
from src.infra.brokers.enums import QueueName


class SendProjectReportUseCase:
    def __init__(self, message_broker: AbstractMessageBroker) -> None:
        self._message_broker = message_broker

    async def execute(self, send_data: ProjectReportData) -> None:
        await self._message_broker.send_message(QueueName.PROJECT_REPORT_NOTIFICATION, send_data)
