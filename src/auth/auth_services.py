from datetime import timedelta, datetime
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import decode, InvalidTokenError, DecodeError, encode
from pydantic import UUID4

from src.auth.auth_enums import AuthTokenTyp
from src.auth.auth_schemas import AuthTokenGet
from src.auth.auth_utils import Hasher
from src.config import settings
from src.user.user_models import UserDB
from src.user.user_repositories import SQLAlchemyUserRepository


class AuthService:
    user_repository: SQLAlchemyUserRepository

    def __init__(self, user_repository: Annotated[SQLAlchemyUserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    def _generate_token(self, sub: UUID4, token_type: AuthTokenTyp, expires_delta: timedelta) -> str:
        expires = datetime.utcnow() + expires_delta
        to_encode = {'exp': expires, 'sub': str(sub), 'typ': token_type}
        return encode(payload=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    async def create_token(self, form_data: OAuth2PasswordRequestForm) -> AuthTokenGet:
        user = await self.user_repository.get_one(username=form_data.username)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if not Hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
            raise HTTPException(status_code=409, detail='Incorrect username or password')

        access_token = self._generate_token(sub=user.id,
                                            token_type=AuthTokenTyp.access,
                                            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
        refresh_token = self._generate_token(sub=user.id,
                                             token_type=AuthTokenTyp.refresh,
                                             expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES))
        return AuthTokenGet(access_token=access_token, refresh_token=refresh_token)

    async def _validate_token(self, token: str, expected_token_typ: AuthTokenTyp) -> UserDB:
        exc = HTTPException(status_code=401, detail='Could not validate credentials')

        try:
            payload = decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = UUID(payload['sub'])
            token_typ = payload['typ']
        except (InvalidTokenError, DecodeError, KeyError, ValueError):
            raise exc

        if token_typ != expected_token_typ:
            raise exc

        user = await self.user_repository.get_one(id=user_id)

        if not user:
            raise exc

        return user

    async def validate_access_token(self, token: str) -> UserDB:
        return await self._validate_token(token=token, expected_token_typ=AuthTokenTyp.access)

    async def refresh_token(self, token: str) -> AuthTokenGet:
        user = await self._validate_token(token=token, expected_token_typ=AuthTokenTyp.refresh)
        access_token = self._generate_token(sub=user.id,
                                            token_type=AuthTokenTyp.access,
                                            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))
        return AuthTokenGet(access_token=access_token)
