from enum import StrEnum


class RabbitMQQueueName(StrEnum):
    DEAD_LETTER = "dlq"
    SEND_PROJECT_REPORT_NOTIFICATION = "project_notifications"


class RabbitMQExchangeName(StrEnum):
    DEAD_LETTER = "dlx"
