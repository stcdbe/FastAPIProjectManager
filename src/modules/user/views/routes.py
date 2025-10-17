from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.auth.dependencies import CurrentUserDep
from src.modules.user.dependencies import validate_user_guid
from src.modules.user.entities.user import User
from src.modules.user.exceptions import InvalidUserDataError
from src.modules.user.services.services import UserService
from src.modules.user.views.schemas import UserCreate, UserGet, UserPatch

user_v1_router = APIRouter(prefix="/users", tags=["Users"])


@user_v1_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGet],
    name="Get some users",
)
async def get_some_users(
    user_service: Annotated[UserService, Depends()],
    page: Annotated[int, Query(default=1, gt=0)],
    limit: Annotated[int, Query(default=5, gt=0, le=10)],
    order_by: Annotated[str, Query(default="username", enum=tuple(UserGet.model_fields))],
    reverse: Annotated[bool, Query(default=False)],
) -> list[User]:
    return await user_service.get_list(
        page=page,
        limit=limit,
        order_by=order_by,
        reverse=reverse,
    )


@user_v1_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=UserGet,
    name="Create a new user",
)
async def create_user(
    user_service: Annotated[UserService, Depends()],
    data: UserCreate,
) -> User:
    try:
        return await user_service.create_one(data=data)
    except InvalidUserDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.msg) from exc


@user_v1_router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserGet,
    name="Get the current user",
)
async def get_me(current_user: CurrentUserDep) -> User:
    return current_user


@user_v1_router.patch(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserGet,
    name="Patch the current user",
)
async def patch_me(
    current_user: CurrentUserDep,
    user_service: Annotated[UserService, Depends()],
    data: UserPatch,
) -> User:
    try:
        return await user_service.patch_one(user=current_user, data=data)
    except InvalidUserDataError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.msg) from exc


@user_v1_router.get(
    path="/{user_guid}",
    status_code=status.HTTP_200_OK,
    response_model=UserGet,
    name="Get the user",
)
async def get_user(user: Annotated[User, Depends(validate_user_guid)]) -> User:
    return user
