from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.common.exc import BaseAppError
from src.domain.user.entities.user import User
from src.domain.user.use_cases.authenticate_user_by_token import AuthenticateUserByTokenUseCase

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/create_token",
    refreshUrl="/api/v1/auth/refresh_token",
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    use_case = AuthenticateUserByTokenUseCase()
    try:
        return await use_case.execute(token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.msg) from e
