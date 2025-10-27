from enum import StrEnum


class RabbitQueueName(StrEnum):
    DLQ = "dlq"
    PROJECT_REPORT_NOTIFICATION = "project_report_notification"


class RabbitExchangeName(StrEnum):
    DLX = "dlx"
