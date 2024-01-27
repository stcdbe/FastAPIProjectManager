from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import decode, InvalidTokenError, DecodeError

from src.auth.authutils import Hasher
from src.config import settings
from src.user.userdependencies import UserServiceDep
from src.user.usermodels import UserDB


TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='api/auth/create_token'))]


async def validate_oauth2_form(user_service: UserServiceDep,
                               form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> UserDB:
    user = await user_service.get_one(username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not Hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
        raise HTTPException(status_code=409, detail='Incorrect username or password')

    return user


async def get_current_user(user_service: UserServiceDep, token: TokenDep) -> UserDB:
    exception = HTTPException(status_code=401, detail='Could not validate credentials')

    try:
        payload = decode(jwt=token,
                         key=settings.JWT_SECRET_KEY,
                         algorithms=[settings.JWT_ALGORITHM])
        user_id = UUID(payload['sub'])
    except (InvalidTokenError, DecodeError, KeyError, ValueError) as e:
        raise exception from e

    if user := await user_service.get_one(id=user_id):
        return user
    raise exception


CurrentUserDep = Annotated[UserDB, Depends(get_current_user)]
