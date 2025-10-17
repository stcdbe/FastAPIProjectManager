from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import UUID4

from src.modules.user.models.entities import User
from src.modules.user.services.services import UserService


async def validate_user_guid(user_service: Annotated[UserService, Depends()], user_guid: UUID4) -> User:
    user = await user_service.get_one(guid=user_guid)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return user
