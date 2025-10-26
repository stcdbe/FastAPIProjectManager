from uuid import UUID

from src.domain.task.exc import TaskNotFoundError
from src.services.task_service import TaskService


class DeleteTaskByGUIDUseCase:
    __slots__ = ("_task_service",)

    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    async def execute(self, project_guid: UUID, task_guid: UUID) -> UUID:
        task = await self._task_service.get_one_by_guid(task_guid)

        if task.project_guid != project_guid:
            msg = f"Project {project_guid} has no task {task_guid}"
            raise TaskNotFoundError(msg)

        return await self._task_service.delete_one(task)
