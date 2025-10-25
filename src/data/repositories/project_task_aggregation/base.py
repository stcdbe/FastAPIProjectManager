from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.project_task_aggregation.entities import ProjectTaskAggregation


class AbstractProjectTaskAggregationRepository(ABC):
    @abstractmethod
    async def get_one_project_with_tasks_by_guid(self, project_guid: UUID) -> ProjectTaskAggregation: ...
