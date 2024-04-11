from typing import Any, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from src.project.project_models import ProjectDB, TaskDB
from src.project.project_repositories import SQLAlchemyProjectRepository
from src.project.project_schemas import ProjectCreate, TaskCreate, ProjectPatch, TaskPatch, ProjectPagination


class ProjectService:
    project_repository: SQLAlchemyProjectRepository

    def __init__(self, project_repository: Annotated[SQLAlchemyProjectRepository, Depends()]) -> None:
        self.project_repository = project_repository

    async def get_list(self, params: ProjectPagination) -> list[ProjectDB]:
        offset = (params.page - 1) * params.limit
        return await self.project_repository.get_list(limit=params.limit,
                                                      offset=offset,
                                                      order_by=params.order_by,
                                                      reverse=params.reverse)

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> ProjectDB | None:
        return await self.project_repository.get_one(load_tasks=load_tasks, **kwargs)

    async def create_one(self, project_data: ProjectCreate, creator_id: UUID) -> ProjectDB | None:
        new_project = ProjectDB(creator_id=creator_id)

        for key, val in project_data.model_dump().items():
            setattr(new_project, key, val)

        return await self.project_repository.create_one(project=new_project)

    async def patch_one(self, project: ProjectDB, upd_project_data: ProjectPatch) -> ProjectDB:
        for key, val in upd_project_data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(project, key, val)

        return await self.project_repository.patch_one(project=project)

    async def del_one(self, project: ProjectDB) -> None:
        await self.project_repository.del_one(project=project)


class TaskService:
    project_repository: SQLAlchemyProjectRepository

    def __init__(self, project_repository: Annotated[SQLAlchemyProjectRepository, Depends()]) -> None:
        self.project_repository = project_repository

    async def create_one(self, project: ProjectDB, task_data: TaskCreate) -> ProjectDB:
        new_task = TaskDB()

        for key, val in task_data.model_dump().items():
            setattr(new_task, key, val)

        project.tasks.append(new_task)
        return await self.project_repository.patch_one(project=project)

    async def patch_one(self,
                        project: ProjectDB,
                        task_id: UUID,
                        upd_task_data: TaskPatch) -> ProjectDB:
        if task_id not in {task.id for task in project.tasks}:
            raise HTTPException(status_code=409, detail='Incorrect task id')

        for task in project.tasks:
            if task.id == task_id:
                for key, val in upd_task_data.model_dump(exclude_none=True, exclude_unset=True).items():
                    setattr(task, key, val)
                break

        return await self.project_repository.patch_one(project=project)

    async def del_one(self, project: ProjectDB, task_id: UUID) -> None:
        if task_id not in {task.id for task in project.tasks}:
            raise HTTPException(status_code=409, detail='Incorrect task id')

        for index, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[index]
                break

        await self.project_repository.patch_one(project=project)
