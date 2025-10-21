from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from pydantic import UUID4

from src.common.exceptions.base import BaseAppError
from src.common.presentation.schemas import GUIDResponse
from src.modules.project.entities.project import Project
from src.modules.project.use_cases.create_project import CreateProjectUseCase
from src.modules.project.use_cases.delete_project_by_guid import DeleteProjectByGUIDUseCase
from src.modules.project.use_cases.get_project_by_guid_by_guid import GetProjectByGUIDUseCase
from src.modules.project.use_cases.get_project_list import GetProjectListUseCase
from src.modules.project.use_cases.patch_project_by_guid import PatchProjectByGUIDUseCase
from src.modules.project.use_cases.send_project_as_report import SendProjectAsReportUseCase
from src.modules.project.views.converters import convert_project_report_send_data_scheme_to_entity
from src.modules.project.views.schemas import (
    ProjectCreateScheme,
    ProjectGetScheme,
    ProjectListGetScheme,
    ProjectPatchScheme,
    ProjectReportSendDataScheme,
)

project_v1_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_v1_router.get(
    path="",
    response_model=ProjectListGetScheme,
    status_code=status.HTTP_200_OK,
    name="Get some projects",
)
async def get_some_projects(
    # _: Annotated[User, Depends(get_current_user)],
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
    name="Crete a new project",
)
async def create_project(
    # _: Annotated[User, Depends(get_current_user)],
    data: ProjectCreateScheme,
) -> dict[str, UUID4]:
    use_case = CreateProjectUseCase()
    try:
        guid = await use_case.execute()

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@project_v1_router.get(
    path="/{project_guid}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectGetScheme,
    name="Get the project",
)
async def get_project_by_guid(
    # _: Annotated[User, Depends(get_current_user)],
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
    name="Patch the project",
)
async def patch_project(
    # _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
    data: ProjectPatchScheme,
) -> dict[str, UUID4]:
    use_case = PatchProjectByGUIDUseCase()
    try:
        guid = await use_case.execute(project_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@project_v1_router.delete(
    path="/{project_guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete the project",
)
async def del_project(
    # _: Annotated[User, Depends(get_current_user)],
    project_guid: UUID4,
) -> None:
    use_case = DeleteProjectByGUIDUseCase()
    try:
        await use_case.execute(project_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@project_v1_router.post(
    path="/{project_guid}/send_as_report",
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=Message,
    name="Send the project report by email",
)
async def send_project_as_report(
    # _: Annotated[User, Depends(get_current_user)],
    scheme_data: ProjectReportSendDataScheme,
) -> None:
    use_case = SendProjectAsReportUseCase()
    send_data = convert_project_report_send_data_scheme_to_entity(scheme_data)
    try:
        return await use_case.execute(send_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


# @project_v1_router.post(
#     path="/{project_guid}/tasks",
#     status_code=status.HTTP_201_CREATED,
#     # response_model=None,
#     name="Add a task to the project",
# )
# async def create_project_task(
#     data: TaskCreate,
# ) -> Project:
#     try:
#         return await task_service.create_one(project=project, data=data)
#     except InvalidProjectDataError as exc:
#         raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message) from exc


# @project_v1_router.patch(
#     path="/{project_guid}/tasks/{task_guid}",
#     status_code=status.HTTP_200_OK,
#     response_model=GUIDResponse,
#     name="Patch the project task",
# )
# async def patch_project_task(
#     # data: TaskPatch,
# ) -> dict[str, UUID4]: ...


# @project_v1_router.delete(
#     path="/{project_guid}/tasks/{task_guid}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     name="Delete the project task",
# )
# async def del_project_task(
#     # _: Annotated[User, Depends(get_current_user)],
# ) -> None: ...
