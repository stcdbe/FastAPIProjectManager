from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database.db import get_session
from src.user.userservice import get_user_db
from src.database.dbmodels import UserDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/create_token')


async def generate_token(user_id: str,
                         expires_delta: timedelta) -> str:
    expires = datetime.utcnow() + expires_delta
    to_encode = {'exp': expires, 'sub': user_id}
    encoded_jwt = jwt.encode(to_encode,
                             key=settings.JWTSECRETKEY,
                             algorithm=settings.JWTALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Annotated[AsyncSession, Depends(get_session)]) -> UserDB:
    exception = HTTPException(status_code=401, detail='Could not validate credentials')

    try:
        payload = jwt.decode(token=token,
                             key=settings.JWTSECRETKEY,
                             algorithms=[settings.JWTALGORITHM])
        user_id = payload['sub']
    except (JWTError, KeyError):
        raise exception

    if user := await get_user_db(session=session, user_id=user_id):
        return user
    raise exception
