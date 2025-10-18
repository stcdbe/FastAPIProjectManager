from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4

from src.modules.auth.exceptions import InvalidAuthDataError
from src.modules.user.entities.user import User
from src.modules.user.services.auth_service import AuthService
from src.modules.user.services.user_service import UserService

TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/create_token"))]


async def get_current_user(auth_service: Annotated[AuthService, Depends()], token: TokenDep) -> User:
    try:
        return await auth_service.validate_access_token(token=token)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=exc.msg) from exc


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def validate_user_guid(user_service: Annotated[UserService, Depends()], user_guid: UUID4) -> User:
    user = await user_service.get_one(guid=user_guid)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return user
