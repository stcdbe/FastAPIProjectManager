from typing import Annotated

from fastapi import HTTPException, Query, Depends
from pydantic import UUID4

from src.user.user_models import UserDB
from src.user.user_schemas import UserGet, UserPagination
from src.user.user_services import UserService

UserServiceDep = Annotated[UserService, Depends()]


async def get_user_list_params(page: Annotated[int, Query(gt=0)] = 1,
                               limit: Annotated[int, Query(gt=0, le=10)] = 5,
                               order_by: Annotated[str, Query(enum=tuple(UserGet.model_fields))] = 'username',
                               reverse: bool = False) -> UserPagination:
    return UserPagination(page=page, limit=limit, order_by=order_by, reverse=reverse)


async def validate_user_id(user_service: UserServiceDep, user_id: UUID4) -> UserDB:
    user = await user_service.get_one(id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user
