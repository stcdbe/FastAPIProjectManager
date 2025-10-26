from uuid import UUID

from src.domain.task.entities import TaskCreateData
from src.services.task_service import TaskService


class CreateTaskUseCase:
    __slots__ = ("_task_service",)

    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    async def execute(self, project_guid: UUID, task_create_data: TaskCreateData) -> UUID:
        return await self._task_service.create_one(project_guid, task_create_data)
