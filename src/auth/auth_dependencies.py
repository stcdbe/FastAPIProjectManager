from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth.auth_services import AuthService
from src.user.user_models import UserDB

AuthServiceDep = Annotated[AuthService, Depends()]
TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='api/auth/create_token'))]


async def get_current_user(auth_service: AuthServiceDep, token: TokenDep) -> UserDB:
    return await auth_service.validate_access_token(token=token)


CurrentUserDep = Annotated[UserDB, Depends(get_current_user)]
