from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, InvalidTokenError, DecodeError

from src.config import settings
from src.dependencies import SQLASessionDep
from src.user.usermodels import UserDB
from src.user.userservice import get_user_db


TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='api/auth/create_token'))]


async def get_current_user(session: SQLASessionDep, token: TokenDep) -> UserDB:
    exception = HTTPException(status_code=401, detail='Could not validate credentials')

    try:
        payload = decode(jwt=token,
                         key=settings.JWT_SECRET_KEY,
                         algorithms=[settings.JWT_ALGORITHM])
        user_id = UUID(payload['sub'])
    except (InvalidTokenError, DecodeError, KeyError, ValueError) as e:
        raise exception from e

    if user := await get_user_db(session=session, id=user_id):
        return user
    raise exception


CurrentUserDep = Annotated[UserDB, Depends(get_current_user)]
