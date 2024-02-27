from typing import Annotated, Any, Awaitable, Callable

from fastapi import HTTPException, Query, Depends
from pydantic import UUID4

from src.auth.auth_dependencies import CurrentUserDep
from src.project.project_models import ProjectDB
from src.project.project_schemas import ProjectGet, ProjectPagination
from src.project.project_services import ProjectService, TaskService

ProjectServiceDep = Annotated[ProjectService, Depends()]
TaskServiceDep = Annotated[TaskService, Depends()]


async def get_project_list_params(page: Annotated[int, Query(gt=0)] = 1,
                                  limit: Annotated[int, Query(gt=0, le=10)] = 5,
                                  order_by: Annotated[str, Query(enum=tuple(ProjectGet.model_fields))] = 'project_title',
                                  reverse: bool = False) -> ProjectPagination:
    return ProjectPagination(page=page,
                             limit=limit,
                             order_by=order_by,
                             reverse=reverse)


class ProjectDepFactory:
    def __init__(self, load_tasks: bool = False) -> None:
        self.load_tasks = load_tasks

    async def __call__(self, project_service: ProjectServiceDep, project_id: UUID4) -> ProjectDB:
        project = await project_service.get_one(load_tasks=self.load_tasks, id=project_id)

        if not project:
            raise HTTPException(status_code=404, detail='Not found')

        return project


def protect_project_dep(load_tasks: bool = False) -> Callable[[ProjectDB, Any], Awaitable[ProjectDB]]:
    async def validate_project_perms(
        current_user: CurrentUserDep,
        project: Annotated[ProjectDB, Depends(ProjectDepFactory(load_tasks=load_tasks))]
    ) -> ProjectDB:
        if current_user.id not in {project.creator_id, project.mentor_id}:
            raise HTTPException(status_code=403, detail='Forbidden request')

        return project

    return validate_project_perms
