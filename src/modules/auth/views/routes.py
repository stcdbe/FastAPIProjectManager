from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.auth.exceptions import InvalidAuthDataError
from src.modules.auth.entities.auth_token import AuthToken
from src.modules.auth.services.services import AuthService
from src.modules.auth.views.schemas import AuthTokenGet

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    path="/create_token",
    status_code=HTTPStatus.CREATED,
    response_model=AuthTokenGet,
    name="Create an access token",
)
async def create_access_token(
    auth_service: Annotated[AuthService, Depends()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthToken:
    try:
        return await auth_service.create_token(form_data=form_data)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=exc.message) from exc


@auth_router.post(
    path="/refresh_token",
    status_code=HTTPStatus.CREATED,
    response_model=AuthToken,
    name="Refresh the access token",
)
async def refresh_access_token(auth_service: Annotated[AuthService, Depends()], token: str) -> AuthToken:
    try:
        return await auth_service.refresh_token(token=token)
    except InvalidAuthDataError as exc:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=exc.message) from exc
