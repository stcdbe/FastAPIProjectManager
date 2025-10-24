from uuid import UUID

from src.domain.task.entities.task import TaskCreateData
from src.services.task_service import TaskService


class CreateTaskUseCase:
    def __init__(self) -> None:
        self._task_service = TaskService()

    async def execute(self, project_guid: UUID, task_create_data: TaskCreateData) -> UUID:
        return await self._task_service.create_one(project_guid, task_create_data)
