from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends, HTTPException, Query
from pydantic import UUID4

from src.modules.auth.dependencies import CurrentUserDep
from src.modules.project.models.entities import Project
from src.modules.project.services.services import ProjectService
from src.modules.project.views.schemas import ProjectGet, ProjectPagination
from src.modules.user.models.entities import User


async def get_project_list_params(
    page: Annotated[int, Query(gt=0)] = 1,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    order_by: Annotated[str, Query(enum=tuple(ProjectGet.model_fields))] = "project_title",
    reverse: bool = False,
) -> ProjectPagination:
    return ProjectPagination(page=page, limit=limit, order_by=order_by, reverse=reverse)


class ProjectDepFactory:
    def __init__(self, load_tasks: bool = False) -> None:
        self.load_tasks = load_tasks

    async def __call__(self, project_service: Annotated[ProjectService, Depends()], project_guid: UUID4) -> Project:
        project = await project_service.get_one(load_tasks=self.load_tasks, guid=project_guid)

        if not project:
            raise HTTPException(status_code=404, detail="Not found")

        return project


def validate_project_perms(load_tasks: bool = False) -> Callable[[User, Project], Awaitable[Project]]:
    async def validate_project_perms(
        current_user: CurrentUserDep,
        project: Annotated[Project, Depends(ProjectDepFactory(load_tasks=load_tasks))],
    ) -> Project:
        if current_user.guid not in {project.creator_guid, project.mentor_guid}:
            raise HTTPException(status_code=403, detail="Forbidden request")

        return project

    return validate_project_perms


async def validate_perms_and_task_guid(
    project: Annotated[Project, Depends(validate_project_perms(load_tasks=True))],
    task_guid: UUID4,
) -> tuple[Project, UUID4]:
    if task_guid not in {task.guid for task in project.tasks}:
        raise HTTPException(status_code=409, detail="Incorrect task id")

    return project, task_guid
