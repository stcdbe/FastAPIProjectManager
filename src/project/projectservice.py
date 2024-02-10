from typing import Any, Annotated
from uuid import UUID

from fastapi import Depends

from src.project.projectmodels import ProjectDB, TaskDB
from src.project.projectrepository import ProjectRepository
from src.project.projectschemas import ProjectCreate, TaskCreate, ProjectPatch, TaskPatch


class ProjectService:
    project_repository: ProjectRepository

    def __init__(self, project_repository: Annotated[ProjectRepository, Depends()]) -> None:
        self.project_repository = project_repository

    async def get_list(self, params: dict[str, Any]) -> list[ProjectDB]:
        offset = (params['page'] - 1) * params['limit']
        return await self.project_repository.get_list(limit=params['limit'],
                                                      offset=offset,
                                                      ordering=params['ordering'],
                                                      reverse=params['reverse'])

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> ProjectDB | None:
        return await self.project_repository.get_one(load_tasks=load_tasks, **kwargs)

    async def create_one(self,
                         project_data: ProjectCreate,
                         creator_id: UUID) -> ProjectDB | None:
        new_project = ProjectDB(creator_id=creator_id)

        for key, val in project_data.model_dump().items():
            setattr(new_project, key, val)

        return await self.project_repository.create_one(project=new_project)

    async def patch_one(self,
                        project: ProjectDB,
                        upd_project_data: ProjectPatch) -> ProjectDB:
        for key, val in upd_project_data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(project, key, val)

        return await self.project_repository.patch_one(project=project)

    async def del_one(self, project: ProjectDB) -> None:
        await self.project_repository.del_one(project=project)

    async def create_task(self,
                          project: ProjectDB,
                          task_data: TaskCreate) -> ProjectDB | None:
        new_task = TaskDB()

        for key, val in task_data.model_dump().items():
            setattr(new_task, key, val)

        project.tasks.append(new_task)
        return await self.project_repository.patch_one(project=project)

    async def patch_task(self,
                         project: ProjectDB,
                         task_id: UUID,
                         upd_task_data: TaskPatch) -> ProjectDB | None:
        for task in project.tasks:
            if task.id == task_id:
                for key, val in upd_task_data.model_dump(exclude_none=True, exclude_unset=True).items():
                    setattr(task, key, val)
                break
        return await self.project_repository.patch_one(project=project)

    async def del_task(self,
                       project: ProjectDB,
                       task_id: UUID) -> None:
        for index, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[index]
                break
        await self.project_repository.patch_one(project=project)
