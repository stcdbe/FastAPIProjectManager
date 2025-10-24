from uuid import UUID

from src.domain.task.exc import TaskInvalidDataError
from src.services.task_service import TaskService


class DeleteTaskByGUIDUseCase:
    def __init__(self) -> None:
        self._task_service = TaskService()

    async def execute(self, project_guid: UUID, task_guid: UUID) -> UUID:
        task = await self._task_service.get_one_by_guid(task_guid)

        if task.project_guid != project_guid:
            msg = "Invalid project guid"
            raise TaskInvalidDataError(msg)

        return await self._task_service.delete_one(task)
