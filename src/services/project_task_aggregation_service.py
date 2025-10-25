from uuid import UUID

from src.data.repositories.project_task_aggregation.sqlalchemy import SQLAlchemyProjectTaskAggregationRepository
from src.domain.project_task_aggregation.entities import ProjectTaskAggregation


class ProjectTaskAggregationService:
    def __init__(self) -> None:
        self._project_task_aggregation_repository = SQLAlchemyProjectTaskAggregationRepository()

    async def get_one_project_with_tasks_by_guid(self, project_guid: UUID) -> ProjectTaskAggregation:
        return await self._project_task_aggregation_repository.get_one_project_with_tasks_by_guid(project_guid)
