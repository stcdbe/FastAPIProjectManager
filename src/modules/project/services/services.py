from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from src.modules.project.models.entities import Project
from src.modules.project.repositories.base import AbstractProjectRepository
from src.modules.project.repositories.sqlachemy import SQLAlchemyProjectRepository
from src.modules.project.views.schemas import ProjectCreate, ProjectPagination, ProjectPatch


class ProjectService:
    _repository: AbstractProjectRepository

    def __init__(self, repository: Annotated[AbstractProjectRepository, Depends(SQLAlchemyProjectRepository)]) -> None:
        self._repository = repository

    async def get_list(self, params: ProjectPagination) -> list[Project]:
        offset = (params.page - 1) * params.limit
        return await self._repository.get_list(
            limit=params.limit,
            offset=offset,
            order_by=params.order_by,
            reverse=params.reverse,
        )

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> Project | None:
        return await self._repository.get_one(load_tasks=load_tasks, **kwargs)

    async def create_one(self, data: ProjectCreate, creator_guid: UUID) -> Project:
        project = Project(creator_guid=creator_guid, **data.model_dump())
        return await self._repository.create_one(project=project)

    async def patch_one(self, project: Project, data: ProjectPatch) -> Project:
        for key, val in data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(project, key, val)
        return await self._repository.patch_one(project=project)

    async def del_one(self, project: Project) -> None:
        await self._repository.del_one(project=project)
