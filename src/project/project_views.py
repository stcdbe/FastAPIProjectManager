from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_cache.decorator import cache
from pydantic import EmailStr, UUID4

from src.auth.auth_dependencies import CurrentUserDep
from src.project.project_dependencies import (get_project_list_params,
                                              ProjectServiceDep,
                                              TaskServiceDep,
                                              ProjectDepFactory,
                                              protect_project_dep)
from src.project.project_models import ProjectDB
from src.project.project_schemas import (ProjectGet,
                                         ProjectCreate,
                                         ProjectWithTasksGet,
                                         TaskCreate,
                                         ProjectPatch,
                                         TaskPatch,
                                         ProjectPagination)
from src.schemas import Message
from src.utils import send_email

project_router = APIRouter(prefix='/projects', tags=['Projects'])


@project_router.get(path='',
                    response_model=list[ProjectGet],
                    status_code=200,
                    name='Get some projects')
@cache(expire=60)
async def get_some_projects(project_service: ProjectServiceDep,
                            params: Annotated[ProjectPagination, Depends(get_project_list_params)]) -> list[ProjectDB]:
    return await project_service.get_list(params=params)


@project_router.post(path='',
                     status_code=201,
                     response_model=ProjectGet,
                     name='Crete a new project')
async def create_project(current_user: CurrentUserDep,
                         project_service: ProjectServiceDep,
                         project_data: ProjectCreate) -> ProjectDB:
    return await project_service.create_one(project_data=project_data, creator_id=current_user.id)


@project_router.get(path='/{project_id}',
                    status_code=200,
                    response_model=ProjectWithTasksGet,
                    name='Get the project')
@cache(expire=60)
async def get_project(project: Annotated[ProjectDB, Depends(ProjectDepFactory(load_tasks=True))]) -> ProjectDB:
    return project


@project_router.post(path='/{project_id}',
                     status_code=201,
                     response_model=ProjectWithTasksGet,
                     name='Add a task to the project')
async def create_project_task(task_service: TaskServiceDep,
                              project: Annotated[ProjectDB, Depends(protect_project_dep(load_tasks=True))],
                              task_data: TaskCreate) -> ProjectDB:
    return await task_service.create_one(project=project, task_data=task_data)


@project_router.patch(path='/{project_id}',
                      status_code=200,
                      response_model=ProjectGet,
                      name='Patch the project')
async def patch_project(project_service: ProjectServiceDep,
                        project: Annotated[ProjectDB, Depends(protect_project_dep())],
                        upd_project_data: ProjectPatch) -> ProjectDB:
    return await project_service.patch_one(project=project, upd_project_data=upd_project_data)


@project_router.delete(path='/{project_id}',
                       status_code=204,
                       name='Delete the project')
async def del_project(project_service: ProjectServiceDep,
                      project: Annotated[ProjectDB, Depends(protect_project_dep())]) -> None:
    await project_service.del_one(project=project)


@project_router.post(path='/{project_id}/send_as_report/{email}',
                     status_code=202,
                     response_model=Message,
                     name='Send the project report by email')
async def send_project_report(current_user: CurrentUserDep,
                              project: Annotated[ProjectDB, Depends(ProjectDepFactory(load_tasks=True))],
                              email: EmailStr,
                              bg_tasks: BackgroundTasks) -> dict[str, str]:
    bg_tasks.add_task(send_email,
                      email_subject='(FastAPIProjectManager) Project report',
                      email_receivers=[email],
                      email_template='projectreportemail.html',
                      **{'project': project})
    return {'message': 'Email sent successfully'}


@project_router.patch(path='/{project_id}/tasks/{task_id}',
                      status_code=200,
                      response_model=ProjectWithTasksGet,
                      name='Patch the project task')
async def patch_project_task(task_service: TaskServiceDep,
                             project: Annotated[ProjectDB, Depends(protect_project_dep(load_tasks=True))],
                             task_id: UUID4,
                             upd_task_data: TaskPatch) -> ProjectDB:
    return await task_service.patch_one(project=project,
                                        task_id=task_id,
                                        upd_task_data=upd_task_data)


@project_router.delete(path='/{project_id}/tasks/{task_id}',
                       status_code=204,
                       name='Delete the project task')
async def del_project_task(task_service: TaskServiceDep,
                           project: Annotated[ProjectDB, Depends(protect_project_dep(load_tasks=True))],
                           task_id: UUID4) -> None:
    await task_service.del_one(project=project, task_id=task_id)
