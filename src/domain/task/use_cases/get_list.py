from uuid import UUID

from src.domain.task.entities import Task
from src.services.task_service import TaskService


class GetTaskListByProjectGUIDUseCase:
    __slots__ = ("_task_service",)

    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    async def execute(self, project_guid: UUID) -> list[Task]:
        return await self._task_service.get_list_by_project_guid(project_guid)
