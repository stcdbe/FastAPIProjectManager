from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import DecodeError, InvalidTokenError, decode, encode

from src.config import settings
from src.modules.auth.exceptions import InvalidAuthDataError
from src.modules.auth.models.entities import AuthToken
from src.modules.auth.models.enums import AuthTokenTyp
from src.modules.auth.utils.hasher import Hasher
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository
from src.modules.user.repositories.sqlalchemy import SQLAlchemyUserRepository


class AuthService:
    _repository: AbstractUserRepository

    def __init__(self, repository: Annotated[AbstractUserRepository, Depends(SQLAlchemyUserRepository)]) -> None:
        self._repository = repository

    def _generate_token(
        self,
        sub: str,
        token_typ: AuthTokenTyp,
        expires_delta: timedelta,
    ) -> str:
        expires = datetime.utcnow() + expires_delta
        to_encode = {"exp": expires, "sub": sub, "typ": token_typ}
        return encode(
            payload=to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    async def create_token(self, form_data: OAuth2PasswordRequestForm) -> AuthToken:
        user = await self._repository.get_one(username=form_data.username)

        if not user:
            raise InvalidAuthDataError(message="User not found")

        if not Hasher.verify_psw(psw_to_check=form_data.password, hashed_psw=user.password):
            raise InvalidAuthDataError(message="Incorrect username or password")

        access_token = self._generate_token(
            sub=str(user.guid),
            token_typ=AuthTokenTyp.access,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
        )
        refresh_token = self._generate_token(
            sub=str(user.guid),
            token_typ=AuthTokenTyp.refresh,
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES),
        )
        return AuthToken(access_token=access_token, refresh_token=refresh_token)

    async def _validate_token(self, token: str, expected_token_typ: AuthTokenTyp) -> User:
        exc = InvalidAuthDataError(message="Could not validate credentials")

        try:
            payload = decode(
                jwt=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            guid = UUID(payload["sub"])
            token_typ = payload["typ"]
        except (InvalidTokenError, DecodeError, KeyError, ValueError):
            raise exc

        if token_typ != expected_token_typ:
            raise exc

        user = await self._repository.get_one(guid=guid)

        if not user:
            raise exc

        return user

    async def validate_access_token(self, token: str) -> User:
        return await self._validate_token(token=token, expected_token_typ=AuthTokenTyp.access)

    async def refresh_token(self, token: str) -> AuthToken:
        user = await self._validate_token(token=token, expected_token_typ=AuthTokenTyp.refresh)
        access_token = self._generate_token(
            sub=str(user.guid),
            token_typ=AuthTokenTyp.access,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
        )
        return AuthToken(access_token=access_token)
