from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.common.exceptions.base import BaseAppError
from src.modules.user.entities.user import User
from src.modules.user.use_cases.authenticate_user_by_token import AuthenticateUserByTokenUseCase


async def get_current_user(
    token: Annotated[
        str,
        Depends(
            OAuth2PasswordBearer(
                tokenUrl="api/v1/auth/create_token",
                refreshUrl="api/v1/auth/refresh_token",
            ),
        ),
    ],
) -> User:
    use_case = AuthenticateUserByTokenUseCase()

    try:
        return await use_case.execute(token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.msg) from e
