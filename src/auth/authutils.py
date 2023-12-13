from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from jwt.exceptions import InvalidTokenError, DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database.db import get_session
from src.user.userservice import get_user_db
from src.database.dbmodels import UserDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/create_token')


async def generate_token(user_id: str, expires_delta: timedelta) -> str:
    expires = datetime.utcnow() + expires_delta
    to_encode = {'exp': expires, 'sub': user_id}
    encoded_jwt = encode(payload=to_encode,
                         key=settings.JWT_SECRET_KEY,
                         algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(session: Annotated[AsyncSession, Depends(get_session)],
                           token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    exception = HTTPException(status_code=401, detail='Could not validate credentials')

    try:
        payload = decode(jwt=token,
                         key=settings.JWT_SECRET_KEY,
                         algorithms=[settings.JWT_ALGORITHM])
        user_id = payload['sub']
    except (InvalidTokenError, DecodeError, KeyError) as e:
        raise exception from e

    if user := await get_user_db(session=session, user_id=user_id):
        return user
    raise exception
