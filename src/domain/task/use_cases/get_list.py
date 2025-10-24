from uuid import UUID

from src.domain.task.entities.task import Task
from src.services.task_service import TaskService


class GetTaskListByProjectGUIDUseCase:
    def __init__(self) -> None:
        self._task_service = TaskService()

    async def execute(self, project_guid: UUID) -> list[Task]:
        return await self._task_service.get_list_by_project_guid(project_guid)
