from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from punq import Container

from src.common.exc import BaseAppError
from src.domain.user.entities import User
from src.domain.user.use_cases.authenticate_user_by_token import AuthenticateUserByTokenUseCase
from src.logic.api_di_container import get_api_di_container

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/create_token",
    refreshUrl="/api/v1/auth/refresh_token",
)


async def get_current_user(
    container: Annotated[Container, Depends(get_api_di_container)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    use_case: AuthenticateUserByTokenUseCase = container.resolve(AuthenticateUserByTokenUseCase)  # type: ignore
    try:
        return await use_case.execute(token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.msg) from e
