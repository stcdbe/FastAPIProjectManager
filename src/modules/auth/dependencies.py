from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.modules.auth.exceptions import InvalidAuthDataError
from src.modules.auth.services.services import AuthService
from src.modules.user.models.entities import User

TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/create_token"))]


async def get_current_user(auth_service: Annotated[AuthService, Depends()], token: TokenDep) -> User:
    try:
        return await auth_service.validate_access_token(token=token)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=401, detail=exc.message) from exc


CurrentUserDep = Annotated[User, Depends(get_current_user)]
