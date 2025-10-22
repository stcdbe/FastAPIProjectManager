from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.common.exc import BaseAppError
from src.domain.user.entities.auth_token import AuthToken
from src.domain.user.use_cases.generate_user_token import GenerateUserTokenUseCase
from src.domain.user.use_cases.refresh_user_token import RefreshUserTokenUseCase
from src.presentation.auth.schemas import AuthTokenScheme

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
    request: Request,
) -> AuthToken:
    use_case = RefreshUserTokenUseCase()
    _, acess_token = request.headers.get("Authorization", "Bearer invalid_token").split(" ")
    try:
        return await use_case.execute(token=acess_token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
