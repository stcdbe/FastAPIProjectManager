from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.authutils import get_current_user
from src.database.db import get_session
from src.database.dbmodels import UserDB
from src.user.userschemas import UserCreate, UserGet, UserPatch
from src.user.userservice import get_some_users_db, create_user_db, get_user_db, patch_user_db

user_router = APIRouter()


@user_router.get('',
                 status_code=200,
                 response_model=list[UserGet],
                 name='Get some user')
@cache(expire=60)
async def get_some_users(session: Annotated[AsyncSession, Depends(get_session)],
                         offset: int = Query(default=0, ge=0),
                         limit: int = Query(default=5, gt=0, le=10),
                         ordering: str = Query('username', enum=list(UserGet.model_fields)),
                         reverse: bool = False) -> Any:
    return await get_some_users_db(session=session,
                                   offset=offset,
                                   limit=limit,
                                   ordering=ordering,
                                   reverse=reverse)


@user_router.post('',
                  status_code=201,
                  response_model=UserGet,
                  name='Create a new user')
async def create_user(session: Annotated[AsyncSession, Depends(get_session)],
                      user_data: UserCreate) -> Any:
    new_user = await create_user_db(user_data=user_data, session=session)

    if not new_user:
        raise HTTPException(status_code=400, detail='The user with this username or email already exists')

    return new_user


@user_router.get('/me',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the current user')
async def get_me(current_user: Annotated[UserDB, Depends(get_current_user)]) -> Any:
    return current_user


@user_router.patch('/me',
                   status_code=200,
                   response_model=UserGet,
                   name='Patch the current user')
async def patch_me(current_user: Annotated[UserDB, Depends(get_current_user)],
                   session: Annotated[AsyncSession, Depends(get_session)],
                   patch_data: UserPatch) -> Any:
    upd_user = await patch_user_db(session=session,
                                   user=current_user,
                                   upd_user_data=patch_data)

    if not upd_user:
        raise HTTPException(status_code=400, detail='Invalid user data')

    return upd_user


@user_router.get('/{user_id}',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the user')
async def get_user(session: Annotated[AsyncSession, Depends(get_session)],
                   user_id: UUID) -> Any:
    user = await get_user_db(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Not found')

    return user
