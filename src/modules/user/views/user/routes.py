from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import UUID4

from src.common.exceptions.base import BaseAppError
from src.common.presentation.schemas import GUIDResponse
from src.modules.user.entities.user import User
from src.modules.user.use_cases.create_user import CreateUserUseCase
from src.modules.user.use_cases.delete_user_by_guid import DeleteUserByGUIDUseCase
from src.modules.user.use_cases.get_one_user_by_guid import GetOneUserByGUIDUseCase
from src.modules.user.use_cases.get_user_list import GetUserListUseCase
from src.modules.user.use_cases.patch_user_by_guid import PatchUserByGUIDUseCase
from src.modules.user.views.user.schemas import UserCreateScheme, UserGetScheme, UserListGetScheme, UserPatchScheme

user_v1_router = APIRouter(prefix="/users", tags=["Users"])


@user_v1_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=UserListGetScheme,
    description="Get user list",
)
async def get_user_list(
    offset: Annotated[int, Query(default=0, gt=0)],
    limit: Annotated[int, Query(default=5, gt=0, le=10)],
    order_by: Annotated[str, Query(default="username", enum=tuple(UserGetScheme.model_fields))],
    reverse: Annotated[bool, Query(default=False)],
) -> dict[str, list[User]]:
    use_case = GetUserListUseCase()
    try:
        users = await use_case.execute()

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"users": users}


@user_v1_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=GUIDResponse,
    description="Create a new user",
)
async def create_user(
    data: UserCreateScheme,
) -> dict[str, UUID4]:
    use_case = CreateUserUseCase()
    try:
        guid = await use_case.execute()

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@user_v1_router.get(
    path="/{user_guid}",
    status_code=status.HTTP_200_OK,
    response_model=UserGetScheme,
    description="Get user by guid",
)
async def get_user(user_guid: UUID4) -> User:
    use_case = GetOneUserByGUIDUseCase()
    try:
        return await use_case.execute(guid=user_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@user_v1_router.patch(
    path="/{user_guid}",
    status_code=status.HTTP_200_OK,
    response_model=GUIDResponse,
    description="Patch user by guid",
)
async def patch_user(
    user_guid: UUID4,
    scheme_data: UserPatchScheme,
) -> dict[str, UUID4]:
    use_case = PatchUserByGUIDUseCase()
    try:
        guid = await use_case.execute()

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@user_v1_router.delete(
    path="/{user_guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete user by guid",
)
async def delete_user(user_guid: UUID4) -> None:
    use_case = DeleteUserByGUIDUseCase()
    try:
        await use_case.execute(guid=user_guid)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
