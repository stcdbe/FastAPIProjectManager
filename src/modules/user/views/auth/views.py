from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.common.exceptions.base import BaseAppError
from src.modules.user.entities.auth_token import AuthToken
from src.modules.user.use_cases.generate_user_token import GenerateUserTokenUseCase
from src.modules.user.use_cases.refresh_user_token import RefreshUserTokenUseCase
from src.modules.user.views.auth.schemas import AuthTokenScheme

auth_v1_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_v1_router.post(
    path="/create_token",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthTokenScheme,
    description="Create an access token",
)
async def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthToken:
    use_case = GenerateUserTokenUseCase()
    try:
        return await use_case.execute(username=form_data.username, password=form_data.password)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@auth_v1_router.post(
    path="/refresh_token",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthTokenScheme,
    description="Refresh the access token",
)
async def refresh_access_token(
    token: str,
) -> AuthToken:
    use_case = RefreshUserTokenUseCase()
    try:
        return await use_case.execute(token=token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
