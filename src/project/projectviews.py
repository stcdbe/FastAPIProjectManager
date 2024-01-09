from typing import Any, Annotated

from fastapi import APIRouter, Query, Depends, HTTPException, BackgroundTasks
from fastapi_cache.decorator import cache
from pydantic import EmailStr, UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.authutils import get_current_user
from src.database.db import get_session
from src.database.dbmodels import UserDB
from src.project.projectschemas import (ProjectGet,
                                        ProjectCreate,
                                        ProjectWithTasksGet,
                                        TaskCreate,
                                        ProjectPatch,
                                        TaskPatch)
from src.schemas import Message
from src.project.projectservice import (get_some_projects_db,
                                        create_project_db,
                                        get_project_with_tasks_db,
                                        get_project_db,
                                        del_project_db,
                                        create_project_task_db,
                                        patch_project_db,
                                        del_project_task_db,
                                        patch_project_task_db)
from src.utils import send_email
from src.user.userservice import get_user_db


project_router = APIRouter()


@project_router.get('',
                    response_model=list[ProjectGet],
                    status_code=200,
                    name='Get some projects')
@cache(expire=60)
async def get_some_projects(session: Annotated[AsyncSession, Depends(get_session)],
                            page: int = Query(default=1, ge=1),
                            limit: int = Query(default=5, gt=0, le=5),
                            ordering: str = Query('project_title', enum=list(ProjectGet.model_fields)),
                            reverse: bool = False) -> Any:
    offset = (page - 1) * limit
    return await get_some_projects_db(session=session,
                                      offset=offset,
                                      limit=limit,
                                      ordering=ordering,
                                      reverse=reverse)


@project_router.post('',
                     status_code=201,
                     response_model=ProjectGet,
                     name='Crete a new project')
async def create_project(current_user: Annotated[UserDB, Depends(get_current_user)],
                         session: Annotated[AsyncSession, Depends(get_session)],
                         project_data: ProjectCreate) -> Any:

    if project_data.mentor_id:
        if not await get_user_db(session=session, user_id=project_data.mentor_id):
            raise HTTPException(status_code=404, detail='Mentor must be registered user')

    return await create_project_db(session=session,
                                   project_data=project_data,
                                   creator_id=current_user.id)


@project_router.get('/{project_id}',
                    status_code=200,
                    response_model=ProjectWithTasksGet,
                    name='Get the project')
@cache(expire=60)
async def get_project(session: Annotated[AsyncSession, Depends(get_session)],
                      project_id: UUID4) -> Any:
    project = await get_project_with_tasks_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    return project


@project_router.post('/{project_id}',
                     status_code=201,
                     response_model=ProjectWithTasksGet,
                     name='Add a task to the project')
async def add_project_task(current_user: Annotated[UserDB, Depends(get_current_user)],
                           session: Annotated[AsyncSession, Depends(get_session)],
                           project_id: UUID4,
                           new_task_data: TaskCreate) -> Any:
    project = await get_project_with_tasks_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    if current_user.id not in {project.creator_id, project.mentor_id}:
        raise HTTPException(status_code=403, detail='Forbidden request')

    if not await get_user_db(session=session, user_id=new_task_data.executor_id):
        raise HTTPException(status_code=404, detail='Task executor must be registered user')

    return await create_project_task_db(session=session,
                                        project=project,
                                        task_data=new_task_data,
                                        executor_id=current_user.id)


@project_router.patch('/{project_id}',
                      status_code=200,
                      response_model=ProjectGet,
                      name='Patch the project')
async def patch_project(current_user: Annotated[UserDB, Depends(get_current_user)],
                        session: Annotated[AsyncSession, Depends(get_session)],
                        project_id: UUID4,
                        upd_project_data: ProjectPatch) -> Any:
    project = await get_project_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    if current_user.id not in {project.creator_id, project.mentor_id}:
        raise HTTPException(status_code=403, detail='Forbidden request')

    if upd_project_data.mentor_id:
        if not await get_user_db(session=session, user_id=upd_project_data.mentor_id):
            raise HTTPException(status_code=404, detail='Mentor must be registered user')

    return await patch_project_db(session=session,
                                  project=project,
                                  upd_project_data=upd_project_data)


@project_router.delete('/{project_id}',
                       status_code=204,
                       name='Delete the project')
async def del_project(current_user: Annotated[UserDB, Depends(get_current_user)],
                      session: Annotated[AsyncSession, Depends(get_session)],
                      project_id: UUID4) -> None:
    project = await get_project_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    if current_user.id not in {project.creator_id, project.mentor_id}:
        raise HTTPException(status_code=403, detail='Forbidden request')

    await del_project_db(session=session, project=project)


@project_router.post('/{project_id}/send_as_report/{email}',
                     status_code=202,
                     response_model=Message,
                     name='Send the project report by email')
async def send_project_report(current_user: Annotated[UserDB, Depends(get_current_user)],
                              session: Annotated[AsyncSession, Depends(get_session)],
                              project_id: UUID4,
                              email: EmailStr,
                              bg_tasks: BackgroundTasks) -> Any:
    project = await get_project_with_tasks_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    bg_tasks.add_task(send_email,
                      email_subject='(FastAPIProjectManager) Project report',
                      email_receivers=[email],
                      email_template='projectreportemail.html',
                      **{'project': project})
    return {'message': 'Email sent successfully'}


@project_router.patch('/{project_id}/tasks/{task_id}',
                      status_code=200,
                      response_model=ProjectWithTasksGet,
                      name='Patch the project task')
async def patch_project_task(current_user: Annotated[UserDB, Depends(get_current_user)],
                             session: Annotated[AsyncSession, Depends(get_session)],
                             project_id: UUID4,
                             task_id: UUID4,
                             upd_task_data: TaskPatch) -> Any:
    project = await get_project_with_tasks_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    if current_user.id not in {project.creator_id, project.mentor_id}:
        raise HTTPException(status_code=403, detail='Forbidden request')

    if task_id not in {task.id for task in project.tasks}:
        raise HTTPException(status_code=409, detail='Incorrect task id')

    if upd_task_data.executor_id:
        if not await get_user_db(session=session, user_id=upd_task_data.executor_id):
            raise HTTPException(status_code=404, detail='Executor not found')

    return await patch_project_task_db(session=session,
                                       project=project,
                                       task_id=task_id,
                                       upd_task_data=upd_task_data)


@project_router.delete('/{project_id}/tasks/{task_id}',
                       status_code=204,
                       name='Delete the project task')
async def del_project_task(current_user: Annotated[UserDB, Depends(get_current_user)],
                           session: Annotated[AsyncSession, Depends(get_session)],
                           project_id: UUID4,
                           task_id: UUID4) -> None:
    project = await get_project_with_tasks_db(session=session, project_id=project_id)

    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    if current_user.id not in {project.creator_id, project.mentor_id}:
        raise HTTPException(status_code=403, detail='Forbidden request')

    if task_id not in {task.id for task in project.tasks}:
        raise HTTPException(status_code=409, detail='Incorrect task id')

    await del_project_task_db(session=session,
                              project=project,
                              task_id=task_id)
