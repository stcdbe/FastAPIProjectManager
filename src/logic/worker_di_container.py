from functools import lru_cache

from punq import Container, Scope

from src.config import get_settings
from src.data.repositories.project_task_aggregation.base import AbstractProjectTaskAggregationRepository
from src.data.repositories.project_task_aggregation.sqlalchemy import SQLAlchemyProjectTaskAggregationRepository
from src.domain.project_task_aggregation.flows.send_project_report_notification import SendProjectReportNotificationFlow
from src.infra.notifications.smtp import SMTPNotificationClient
from src.services.project_task_aggregation_service import ProjectTaskAggregationService


def _get_worker_di_container() -> Container:
    container = Container()
    # repos
    container.register(
        AbstractProjectTaskAggregationRepository,
        factory=lambda: SQLAlchemyProjectTaskAggregationRepository(get_settings().PG_URL.unicode_string()),
        scope=Scope.singleton,
    )
    # infra
    container.register(SMTPNotificationClient, scope=Scope.singleton)
    # services
    container.register(ProjectTaskAggregationService)
    # project task aggregation flows
    container.register(SendProjectReportNotificationFlow)

    return container


@lru_cache(maxsize=1)
def get_worker_di_container() -> Container:
    return _get_worker_di_container()
