from uuid import UUID

from src.data.repositories.project_task_aggregation.base import AbstractProjectTaskAggregationRepository
from src.domain.project_task_aggregation.entities import ProjectTaskAggregation


class ProjectTaskAggregationService:
    __slots__ = ("_project_task_aggregation_repository",)

    def __init__(
        self,
        project_task_aggregation_repository: AbstractProjectTaskAggregationRepository,
    ) -> None:
        self._project_task_aggregation_repository = project_task_aggregation_repository

    async def get_one_project_with_tasks_by_guid(self, project_guid: UUID) -> ProjectTaskAggregation:
        return await self._project_task_aggregation_repository.get_one_project_with_tasks_by_guid(project_guid)
