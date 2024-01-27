from typing import Annotated, Any

from fastapi import HTTPException, Query, Depends
from pydantic import UUID4

from src.project.projectmodels import ProjectDB
from src.project.projectschemas import ProjectGet
from src.project.projectservice import ProjectService


ProjectServiceDep = Annotated[ProjectService, Depends()]


async def get_project_list_params(page: Annotated[int, Query(gt=0)] = 1,
                                  limit: Annotated[int, Query(gt=0, le=10)] = 5,
                                  ordering: Annotated[str, Query(enum=list(ProjectGet.model_fields))] = 'project_title',
                                  reverse: bool = False) -> dict[str, Any]:
    return {'page': page,
            'limit': limit,
            'ordering': ordering,
            'reverse': reverse}


async def validate_project_id(project_service: ProjectServiceDep, project_id: UUID4) -> ProjectDB:
    project = await project_service.get_one(id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Not found')

    return project


async def validate_project_with_tasks_id(project_service: ProjectServiceDep, project_id: UUID4) -> ProjectDB:
    project = await project_service.get_one(load_tasks=True, id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Not found')

    return project
