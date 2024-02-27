from datetime import timedelta, datetime
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import decode, InvalidTokenError, DecodeError, encode

from src.auth.auth_utils import Hasher
from src.config import settings
from src.user.user_models import UserDB
from src.user.user_repositories import UserRepository


class AuthService:
    user_repository: UserRepository

    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    async def create_token(self, form_data: OAuth2PasswordRequestForm) -> dict[str, str]:
        user = await self.user_repository.get_one(username=form_data.username)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if not Hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
            raise HTTPException(status_code=409, detail='Incorrect username or password')

        expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
        to_encode = {'exp': expires, 'sub': str(user.id)}
        token = encode(payload=to_encode,
                       key=settings.JWT_SECRET_KEY,
                       algorithm=settings.JWT_ALGORITHM)
        return {'access_token': token, 'token_type': 'bearer'}

    async def validate_token(self, token: str) -> UserDB:
        exc = HTTPException(status_code=401, detail='Could not validate credentials')

        try:
            payload = decode(jwt=token,
                             key=settings.JWT_SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
            user_id = UUID(payload['sub'])
        except (InvalidTokenError, DecodeError, KeyError, ValueError):
            raise exc

        user = await self.user_repository.get_one(id=user_id)

        if not user:
            raise exc

        return user
