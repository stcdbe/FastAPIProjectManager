from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.modules.auth.dependencies import CurrentUserDep
from src.modules.user.dependencies import get_user_list_params, validate_user_guid
from src.modules.user.exceptions import InvalidUserDataError
from src.modules.user.models.entities import User
from src.modules.user.services.services import UserService
from src.modules.user.views.schemas import UserCreate, UserGet, UserPagination, UserPatch

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get(
    path="",
    status_code=200,
    response_model=list[UserGet],
    name="Get some users",
)
async def get_some_users(
    user_service: Annotated[UserService, Depends()],
    params: Annotated[UserPagination, Depends(get_user_list_params)],
) -> list[User]:
    return await user_service.get_list(params=params)


@user_router.post(
    path="",
    status_code=201,
    response_model=UserGet,
    name="Create a new user",
)
async def create_user(user_service: Annotated[UserService, Depends()], data: UserCreate) -> User:
    try:
        return await user_service.create_one(data=data)
    except InvalidUserDataError as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@user_router.get(
    path="/me",
    status_code=200,
    response_model=UserGet,
    name="Get the current user",
)
async def get_me(current_user: CurrentUserDep) -> User:
    return current_user


@user_router.patch(
    path="/me",
    status_code=200,
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
        raise HTTPException(status_code=409, detail=exc.message)


@user_router.get(
    path="/{user_guid}",
    status_code=200,
    response_model=UserGet,
    name="Get the user",
)
async def get_user(user: Annotated[User, Depends(validate_user_guid)]) -> User:
    return user
