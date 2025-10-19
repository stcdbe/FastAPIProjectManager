from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import UUID4

from src.common.exceptions.base import BaseAppError
from src.common.presentation.schemas import GUIDResponse
from src.modules.user.dependencies import get_current_user
from src.modules.user.entities.user import User
from src.modules.user.exc import UserNotFoundError
from src.modules.user.use_cases.create_user import CreateUserUseCase
from src.modules.user.use_cases.delete_user_by_guid import DeleteUserByGUIDUseCase
from src.modules.user.use_cases.get_one_user_by_guid import GetOneUserByGUIDUseCase
from src.modules.user.use_cases.get_user_list import GetUserListUseCase
from src.modules.user.use_cases.patch_user_by_guid import PatchUserByGUIDUseCase
from src.modules.user.views.user.converters import (
    convert_user_create_data_scheme_to_entity,
    convert_user_patch_data_scheme_to_entity,
)
from src.modules.user.views.user.schemas import UserCreateScheme, UserGetScheme, UserListGetScheme, UserPatchScheme

user_v1_router = APIRouter(prefix="/users", tags=["Users"])


@user_v1_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=UserListGetScheme,
    description="Get user list",
)
async def get_user_list(
    # _: Annotated[User, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    order_by: Annotated[str, Query(enum=tuple(UserGetScheme.model_fields))] = "username",
    reverse: Annotated[bool, Query()] = False,
) -> dict[str, list[User]]:
    use_case = GetUserListUseCase()
    try:
        users = await use_case.execute(offset, limit, order_by, reverse)

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
    # _: Annotated[User, Depends(get_current_user)],
    scheme_data: UserCreateScheme,
) -> dict[str, UUID4]:
    use_case = CreateUserUseCase()
    user_create_data = convert_user_create_data_scheme_to_entity(scheme_data)
    try:
        guid = await use_case.execute(user_create_data)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@user_v1_router.get(
    path="/{user_guid}",
    status_code=status.HTTP_200_OK,
    response_model=UserGetScheme,
    description="Get user by guid",
)
async def get_user(
    # _: Annotated[User, Depends(get_current_user)],
    user_guid: UUID4,
) -> User:
    use_case = GetOneUserByGUIDUseCase()
    try:
        return await use_case.execute(guid=user_guid)

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg) from e

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@user_v1_router.patch(
    path="/{user_guid}",
    status_code=status.HTTP_200_OK,
    response_model=GUIDResponse,
    description="Patch user by guid",
)
async def patch_user(
    # _: Annotated[User, Depends(get_current_user)],
    user_guid: UUID4,
    scheme_data: UserPatchScheme,
) -> dict[str, UUID4]:
    use_case = PatchUserByGUIDUseCase()
    user_patch_data = convert_user_patch_data_scheme_to_entity(scheme_data)
    try:
        guid = await use_case.execute(user_guid, user_patch_data)

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg) from e

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e

    return {"guid": guid}


@user_v1_router.delete(
    path="/{user_guid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete user by guid",
)
async def delete_user(
    # _: Annotated[User, Depends(get_current_user)],
    user_guid: UUID4,
) -> None:
    use_case = DeleteUserByGUIDUseCase()
    try:
        await use_case.execute(guid=user_guid)

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg) from e

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
