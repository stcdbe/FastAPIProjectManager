from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.auth.authdependencies import CurrentUserDep
from src.dependencies import SQLASessionDep
from src.user.userdependencies import validate_user_id, get_user_list_params
from src.user.usermodels import UserDB
from src.user.userschemas import UserCreate, UserGet, UserPatch
from src.user.userservice import create_user_db, get_some_users_db, patch_user_db

user_router = APIRouter()


@user_router.get('',
                 status_code=200,
                 response_model=list[UserGet],
                 name='Get some users')
@cache(expire=60)
async def get_some_users(session: SQLASessionDep,
                         params: Annotated[dict[str, Any], Depends(get_user_list_params)]) -> list[UserDB]:
    return await get_some_users_db(session=session,
                                   offset=params['offset'],
                                   limit=params['limit'],
                                   ordering=params['ordering'],
                                   reverse=params['reverse'])


@user_router.post('',
                  status_code=201,
                  response_model=UserGet,
                  name='Create a new user')
async def create_user(session: SQLASessionDep,
                      user_data: UserCreate) -> UserDB:
    new_user = await create_user_db(session=session, user_data=user_data)

    if not new_user:
        raise HTTPException(status_code=409, detail='The user with this username or email already exists')

    return new_user


@user_router.get('/me',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the current user')
async def get_me(current_user: CurrentUserDep) -> UserDB:
    return current_user


@user_router.patch('/me',
                   status_code=200,
                   response_model=UserGet,
                   name='Patch the current user')
async def patch_me(current_user: CurrentUserDep,
                   session: SQLASessionDep,
                   patch_data: UserPatch) -> UserDB:
    upd_user = await patch_user_db(session=session, user=current_user, upd_user_data=patch_data)

    if not upd_user:
        raise HTTPException(status_code=409, detail='The user with this username or email already exists')

    return upd_user


@user_router.get('/{user_id}',
                 status_code=200,
                 response_model=UserGet,
                 name='Get the user')
async def get_user(user: Annotated[UserDB, Depends(validate_user_id)]) -> UserDB:
    return user
