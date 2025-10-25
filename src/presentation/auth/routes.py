from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.common.exc import BaseAppError
from src.domain.user.entities import AuthToken, User
from src.domain.user.exc import UserInvalidCredentialsError, UserNotFoundError
from src.domain.user.use_cases.generate_user_token import GenerateUserTokenUseCase
from src.domain.user.use_cases.refresh_user_token import RefreshUserTokenUseCase
from src.presentation.auth.schemas import AuthTokenScheme, RefreshTokenInputScheme
from src.presentation.common.schemas import ErrorResponse
from src.presentation.dependencies import get_current_user

auth_v1_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_v1_router.post(
    path="/create_token",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthTokenScheme,
    description="Create an access token",
    responses={
        status.HTTP_201_CREATED: {"model": AuthTokenScheme},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthToken:
    use_case = GenerateUserTokenUseCase()
    try:
        return await use_case.execute(username=form_data.username, password=form_data.password)

    except (UserNotFoundError, UserInvalidCredentialsError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.msg,
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e


@auth_v1_router.post(
    path="/refresh_token",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthTokenScheme,
    description="Refresh the access token",
    responses={
        status.HTTP_201_CREATED: {"model": AuthTokenScheme},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def refresh_token(
    _: Annotated[User, Depends(get_current_user)],
    sheme_data: RefreshTokenInputScheme,
) -> AuthToken:
    use_case = RefreshUserTokenUseCase()
    try:
        return use_case.execute(sheme_data.refresh_token)

    except BaseAppError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg) from e
