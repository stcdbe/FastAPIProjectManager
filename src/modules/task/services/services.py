from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.modules.project.models.entities import Project
from src.modules.project.repositories.base import AbstractProjectRepository
from src.modules.project.repositories.sqlachemy import SQLAlchemyProjectRepository
from src.modules.task.models.entities import Task
from src.modules.task.views.schemas import TaskCreate, TaskPatch


class TaskService:
    _repository: AbstractProjectRepository

    def __init__(self, repository: Annotated[AbstractProjectRepository, Depends(SQLAlchemyProjectRepository)]) -> None:
        self._repository = repository

    async def create_one(self, project: Project, data: TaskCreate) -> Project:
        task = Task(**data.model_dump())
        project.tasks.append(task)
        return await self._repository.patch_one(project=project)

    async def patch_one(
        self,
        project: Project,
        task_guid: UUID,
        data: TaskPatch,
    ) -> Project:
        for task in project.tasks:
            if task.guid == task_guid:
                for key, val in data.model_dump(exclude_none=True, exclude_unset=True).items():
                    setattr(task, key, val)
                break
        return await self._repository.patch_one(project=project)

    async def del_one(self, project: Project, task_guid: UUID) -> None:
        for index, task in enumerate(project.tasks):
            if task.guid == task_guid:
                del project.tasks[index]
                break
        await self._repository.patch_one(project=project)
