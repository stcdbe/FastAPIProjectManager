from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth_dependencies import AuthServiceDep
from src.auth.auth_schemas import AuthTokenGet

login_router = APIRouter(prefix='/auth', tags=['Auth'])


@login_router.post(path='/create_token',
                   status_code=201,
                   response_model=AuthTokenGet,
                   name='Create an access token')
async def create_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                              auth_service: AuthServiceDep) -> AuthTokenGet:
    return await auth_service.create_token(form_data=form_data)


@login_router.post(path='/refresh_token',
                   status_code=201,
                   response_model=AuthTokenGet,
                   name='Refresh the access token')
async def refresh_access_token(token: str, auth_service: AuthServiceDep) -> AuthTokenGet:
    return await auth_service.refresh_token(token=token)
