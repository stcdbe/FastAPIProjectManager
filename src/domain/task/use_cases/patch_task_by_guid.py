from uuid import UUID

from src.domain.task.entities import TaskPatchData
from src.domain.task.exc import TaskInvalidDataError
from src.services.task_service import TaskService


class PatchTaskByGUIDUseCase:
    __slots__ = ("_task_service",)

    def __init__(self, task_service: TaskService) -> None:
        self._task_service = task_service

    async def execute(self, project_guid: UUID, task_guid: UUID, task_patch_data: TaskPatchData) -> UUID:
        task = await self._task_service.get_one_by_guid(task_guid)

        if task.project_guid != project_guid:
            msg = "Invalid project guid"
            raise TaskInvalidDataError(msg)

        return await self._task_service.patch_one(task, task_patch_data)
