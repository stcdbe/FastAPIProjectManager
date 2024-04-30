from typing import Annotated

from fastapi import Depends, HTTPException, Query
from pydantic import UUID4

from src.modules.user.models.entities import User
from src.modules.user.services.services import UserService
from src.modules.user.views.schemas import UserGet, UserPagination


async def get_user_list_params(
    page: Annotated[int, Query(gt=0)] = 1,
    limit: Annotated[int, Query(gt=0, le=10)] = 5,
    order_by: Annotated[str, Query(enum=tuple(UserGet.model_fields))] = "username",
    reverse: bool = False,
) -> UserPagination:
    return UserPagination(page=page, limit=limit, order_by=order_by, reverse=reverse)


async def validate_user_guid(user_service: Annotated[UserService, Depends()], user_guid: UUID4) -> User:
    user = await user_service.get_one(guid=user_guid)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
