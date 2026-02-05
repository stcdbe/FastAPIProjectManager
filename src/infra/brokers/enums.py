from enum import StrEnum


class QueueName(StrEnum):
    DLQ = "dlq"
    PROJECT_REPORT_NOTIFICATION = "project_report_notification"


class ExchangeName(StrEnum):
    DLX = "dlx"
