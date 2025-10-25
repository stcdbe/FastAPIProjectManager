from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.data.repositories.task.sqlalchemy import SQLAlchemyTaskRepository
from src.domain.task.entities.task import Task, TaskCreateData, TaskPatchData


class TaskService:
    __slots__ = ("_task_repository",)

    def __init__(self) -> None:
        self._task_repository = SQLAlchemyTaskRepository()

    async def get_list_by_project_guid(self, project_guid: UUID) -> list[Task]:
        return await self._task_repository.get_list_by_project_guid(project_guid)

    async def get_one_by_guid(self, guid: UUID) -> Task:
        return await self._task_repository.get_one_by_guid(guid)

    async def create_one(self, project_guid: UUID, task_create_data: TaskCreateData) -> UUID:
        task = Task(
            guid=uuid4(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            title=task_create_data.title,
            description=task_create_data.description,
            is_completed=task_create_data.is_completed,
            project_guid=project_guid,
            executor_guid=task_create_data.executor_guid,
        )
        return await self._task_repository.create_one(task)

    async def patch_one(self, task: Task, task_patch_data: TaskPatchData) -> UUID:
        if task_patch_data.title is not None:
            task.title = task_patch_data.title

        if task_patch_data.description is not None:
            task.description = task_patch_data.description

        if task_patch_data.is_completed is not None:
            task.is_completed = task_patch_data.is_completed

        if task_patch_data.executor_guid is not None:
            task.executor_guid = task_patch_data.executor_guid

        task.updated_at = datetime.now(UTC)
        return await self._task_repository.patch_one(task)

    async def delete_one(self, task: Task) -> UUID:
        return await self._task_repository.delete_one(task)
