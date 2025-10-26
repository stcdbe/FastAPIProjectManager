from src.domain.project.entities import ProjectReportData
from src.infra.worker.broker import RabbitMQMessageBroker
from src.infra.worker.enums import RabbitMQQueueName


class SendProjectReportUseCase:
    def __init__(self, message_broker: RabbitMQMessageBroker) -> None:
        self._message_broker = message_broker

    async def execute(self, send_data: ProjectReportData) -> None:
        await self._message_broker.send_message(RabbitMQQueueName.SEND_PROJECT_REPORT_NOTIFICATION, send_data)
