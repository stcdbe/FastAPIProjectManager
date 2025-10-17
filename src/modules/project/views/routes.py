from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import UUID4, EmailStr

from src.common.presentation.schemas import Message
from src.common.utils.email.smtp import send_email
from src.modules.auth.dependencies import CurrentUserDep
from src.modules.project.dependencies import (
    ProjectDepFactory,
    get_project_list_params,
    validate_perms_and_task_guid,
    validate_project_perms,
)
from src.modules.project.exceptions import InvalidProjectDataError
from src.modules.project.models.entities import Project
from src.modules.project.services.project_service import ProjectService
from src.modules.project.views.schemas import (
    ProjectCreate,
    ProjectGet,
    ProjectPagination,
    ProjectPatch,
    ProjectWithTasksGet,
)
from src.modules.task.services.services import TaskService
from src.modules.task.views.schemas import TaskCreate, TaskPatch

project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.get(
    path="",
    response_model=list[ProjectGet],
    status_code=HTTPStatus.OK,
    name="Get some projects",
)
async def get_some_projects(
    project_service: Annotated[ProjectService, Depends()],
    params: Annotated[ProjectPagination, Depends(get_project_list_params)],
) -> list[Project]:
    return await project_service.get_list(params=params)


@project_router.post(
    path="",
    status_code=HTTPStatus.CREATED,
    response_model=ProjectGet,
    name="Crete a new project",
)
async def create_project(
    current_user: CurrentUserDep,
    project_service: Annotated[ProjectService, Depends()],
    data: ProjectCreate,
) -> Project:
    try:
        return await project_service.create_one(data=data, creator_guid=current_user.guid)
    except InvalidProjectDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message) from exc


@project_router.get(
    path="/{project_guid}",
    status_code=HTTPStatus.OK,
    response_model=ProjectWithTasksGet,
    name="Get the project",
)
async def get_project(project: Annotated[Project, Depends(ProjectDepFactory(load_tasks=True))]) -> Project:
    return project


@project_router.post(
    path="/{project_guid}",
    status_code=HTTPStatus.CREATED,
    response_model=ProjectWithTasksGet,
    name="Add a task to the project",
)
async def create_project_task(
    task_service: Annotated[TaskService, Depends()],
    project: Annotated[Project, Depends(validate_project_perms(load_tasks=True))],
    data: TaskCreate,
) -> Project:
    try:
        return await task_service.create_one(project=project, data=data)
    except InvalidProjectDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message) from exc


@project_router.patch(
    path="/{project_guid}",
    status_code=HTTPStatus.OK,
    response_model=ProjectGet,
    name="Patch the project",
)
async def patch_project(
    project_service: Annotated[ProjectService, Depends()],
    project: Annotated[Project, Depends(validate_project_perms())],
    data: ProjectPatch,
) -> Project:
    try:
        return await project_service.patch_one(project=project, data=data)
    except InvalidProjectDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message) from exc


@project_router.delete(
    path="/{project_guid}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Delete the project",
)
async def del_project(
    project_service: Annotated[ProjectService, Depends()],
    project: Annotated[Project, Depends(validate_project_perms())],
) -> None:
    await project_service.del_one(project=project)


@project_router.post(
    path="/{project_guid}/send_as_report/{email}",
    status_code=HTTPStatus.ACCEPTED,
    response_model=Message,
    name="Send the project report by email",
)
async def send_project_report(
    _: CurrentUserDep,
    project: Annotated[Project, Depends(ProjectDepFactory(load_tasks=True))],
    email: EmailStr,
    bg_tasks: BackgroundTasks,
) -> dict[str, str]:
    bg_tasks.add_task(
        send_email,
        email_subject="(FastAPIProjectManager) Project report",
        email_receivers=[email],
        email_template="projectreportemail.html",
        project=project,
    )
    return {"message": "Email sent successfully"}


@project_router.patch(
    path="/{project_guid}/tasks/{task_guid}",
    status_code=HTTPStatus.OK,
    response_model=ProjectWithTasksGet,
    name="Patch the project task",
)
async def patch_project_task(
    task_service: Annotated[TaskService, Depends()],
    project_and_task_guid: Annotated[tuple[Project, UUID4], Depends(validate_perms_and_task_guid)],
    data: TaskPatch,
) -> Project:
    project, task_guid = project_and_task_guid
    try:
        return await task_service.patch_one(
            project=project,
            task_guid=task_guid,
            data=data,
        )
    except InvalidProjectDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message) from exc


@project_router.delete(
    path="/{project_guid}/tasks/{task_guid}",
    status_code=HTTPStatus.NO_CONTENT,
    name="Delete the project task",
)
async def del_project_task(
    task_service: Annotated[TaskService, Depends()],
    project_and_task_guid: Annotated[tuple[Project, UUID4], Depends(validate_perms_and_task_guid)],
) -> None:
    project, task_id = project_and_task_guid
    await task_service.del_one(project=project, task_guid=task_id)
