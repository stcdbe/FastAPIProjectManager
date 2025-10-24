from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from pydantic import UUID4

from src.common.exc import BaseAppError
from src.domain.project.entities.project import Project
from src.domain.project.use_cases.create_project import CreateProjectUseCase
from src.domain.project.use_cases.delete_project_by_guid import DeleteProjectByGUIDUseCase
from src.domain.project.use_cases.get_project_by_guid_by_guid import GetProjectByGUIDUseCase
from src.domain.project.use_cases.get_project_list import GetProjectListUseCase
from src.domain.project.use_cases.patch_project_by_guid import PatchProjectByGUIDUseCase
from src.domain.project.use_cases.send_project_as_report import SendProjectAsReportUseCase
from src.domain.task.entities.task import Task
from src.domain.task.use_cases.create_task import CreateTaskUseCase
from src.domain.task.use_cases.delete_task_by_guid import DeleteTaskByGUIDUseCase
from src.domain.task.use_cases.get_list import GetTaskListByProjectGUIDUseCase
from src.domain.task.use_cases.patch_task_by_guid import PatchTaskByGUIDUseCase
from src.domain.user.entities.user import User
from src.presentation.common.schemas import ErrorResponse, GUIDResponse
from src.presentation.dependencies import get_current_user
from src.presentation.project.converters import (
    convert_project_create_scheme_to_entity,
    convert_project_patch_scheme_to_entity,
    convert_project_report_send_data_scheme_to_entity,
)
from src.presentation.project.schemas import (
    ProjectCreateScheme,
    ProjectGetScheme,
    ProjectListGetScheme,
    ProjectPatchScheme,
    ProjectReportSendDataScheme,
)
from src.presentation.task.converters import convert_task_create_scheme_to_entity, convert_task_patch_scheme_to_entity
from src.presentation.task.schemas import TaskCreateScheme, TaskListGetScheme, TaskPatchScheme

project_v1_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_v1_router.get(
    path="",
    response_model=ProjectListGetScheme,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ProjectListGetScheme},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Get project list",
)
async def get_project_list(
    _: Annotated[User, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    order_by: Annotated[str, Query(enum=tuple(ProjectGetScheme.model_fields))] = "created_at",
    reverse: Annotated[bool, Query()] = False,
) -> dict[str, list[Project]]:
    use_case = GetProjectListUseCase()
    try:
        projects = await use_case.execute(offset, limit, order_by, reverse)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"projects": projects}


@project_v1_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=GUIDResponse,
    responses={
        status.HTTP_201_CREATED: {"model": GUIDResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Crete a new project",
)
async def create_project(
    current_user: Annotated[User, Depends(get_current_user)],
    scheme_data: ProjectCreateScheme,
) -> dict[str, UUID4]:
    use_case = CreateProjectUseCase()
    project_create_data = convert_project_create_scheme_to_entity(scheme_data)
    try:
        guid = await use_case.execute(current_user, project_create_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@project_v1_router.get(
    path="/{project_guid}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectGetScheme,
    responses={
        status.HTTP_200_OK: {"model": ProjectGetScheme},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    description="Get the project",
)
async def get_project(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
) -> Project:
    use_case = GetProjectByGUIDUseCase()
    try:
        return await use_case.execute(project_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@project_v1_router.patch(
    path="/{project_guid}",
    status_code=status.HTTP_200_OK,
    response_model=GUIDResponse,
    responses={
        status.HTTP_200_OK: {"model": GUIDResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    description="Patch the project",
)
async def patch_project(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
    scheme_data: ProjectPatchScheme,
) -> dict[str, UUID4]:
    use_case = PatchProjectByGUIDUseCase()
    project_patch_data = convert_project_patch_scheme_to_entity(scheme_data)
    try:
        guid = await use_case.execute(project_guid, project_patch_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@project_v1_router.delete(
    path="/{project_guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    description="Delete the project",
)
async def delete_project(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
) -> None:
    use_case = DeleteProjectByGUIDUseCase()
    try:
        await use_case.execute(project_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@project_v1_router.post(
    path="/send_as_report",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=None,
    responses={
        status.HTTP_202_ACCEPTED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Send the project report by email",
)
async def send_project_report(
    _: Annotated[User, Depends(get_current_user)],
    scheme_data: ProjectReportSendDataScheme,
) -> None:
    use_case = SendProjectAsReportUseCase()
    send_data = convert_project_report_send_data_scheme_to_entity(scheme_data)
    try:
        await use_case.execute(send_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@project_v1_router.get(
    path="/{project_guid}/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TaskListGetScheme,
    responses={
        status.HTTP_200_OK: {"model": TaskListGetScheme},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Get project tasks",
)
async def get_task_list(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
) -> dict[str, list[Task]]:
    use_case = GetTaskListByProjectGUIDUseCase()
    try:
        res = await use_case.execute(project_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"tasks": res}


@project_v1_router.post(
    path="/{project_guid}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=GUIDResponse,
    responses={
        status.HTTP_201_CREATED: {"model": GUIDResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Add a task to the project",
)
async def create_task(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
    scheme_data: TaskCreateScheme,
) -> dict[str, UUID4]:
    use_case = CreateTaskUseCase()
    task_create_data = convert_task_create_scheme_to_entity(scheme_data)
    try:
        res = await use_case.execute(project_guid, task_create_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": res}


@project_v1_router.patch(
    path="/{project_guid}/tasks/{task_guid}",
    status_code=status.HTTP_200_OK,
    response_model=GUIDResponse,
    responses={
        status.HTTP_200_OK: {"model": GUIDResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Patch the project task",
)
async def patch_task(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
    task_guid: UUID4,
    scheme_data: TaskPatchScheme,
) -> dict[str, UUID4]:
    use_case = PatchTaskByGUIDUseCase()
    task_patch_data = convert_task_patch_scheme_to_entity(scheme_data)
    try:
        res = await use_case.execute(project_guid, task_guid, task_patch_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": res}


@project_v1_router.delete(
    path="/{project_guid}/tasks/{task_guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
    },
    description="Delete the project task",
)
async def delete_task(
    _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
    task_guid: UUID4,
) -> None:
    use_case = DeleteTaskByGUIDUseCase()
    try:
        await use_case.execute(project_guid, task_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
