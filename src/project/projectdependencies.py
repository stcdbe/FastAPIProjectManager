from typing import Annotated, Any

from fastapi import HTTPException, Query
from pydantic import UUID4

from src.dependencies import SQLASessionDep
from src.project.projectmodels import ProjectDB
from src.project.projectschemas import ProjectGet
from src.project.projectservice import get_project_db


async def get_project_list_params(page: Annotated[int, Query(gt=0)] = 1,
                                  limit: Annotated[int, Query(gt=0, le=10)] = 5,
                                  ordering: Annotated[str, Query(enum=list(ProjectGet.model_fields))] = 'project_title',
                                  reverse: bool = False) -> dict[str, Any]:
    offset = (page - 1) * limit
    return {'offset': offset,
            'limit': limit,
            'ordering': ordering,
            'reverse': reverse}


async def validate_project_id(session: SQLASessionDep, project_id: UUID4) -> ProjectDB:
    project = await get_project_db(session=session, id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Not found')

    return project


async def validate_project_with_tasks_id(session: SQLASessionDep, project_id: UUID4) -> ProjectDB:
    project = await get_project_db(session=session,
                                   get_tasks=True,
                                   id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Not found')

    return project
