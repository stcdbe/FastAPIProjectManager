from typing import Annotated, Any

from fastapi import Depends

from src.modules.auth.utils.hasher.base import AbstractHasher
from src.modules.user.services.hasher_service import BcryptHasher
from src.modules.user.data.repositories.base import AbstractUserRepository
from src.modules.user.data.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.user.entities.user import User


class UserService:
    _repository: AbstractUserRepository
    _hasher: AbstractHasher

    def __init__(
        self,
        repository: Annotated[AbstractUserRepository, Depends(SQLAlchemyUserRepository)],
        hasher: Annotated[AbstractHasher, Depends(BcryptHasher)],
    ) -> None:
        self._repository = repository
        self._hasher = hasher

    async def get_one(self, **kwargs: Any) -> User | None:
        return await self._repository.get_one(**kwargs)

    async def get_list(
        self,
        page: int = 1,
        limit: int = 5,
        order_by: str = "username",
        reverse: bool = False,
    ) -> list[User]:
        offset = (page - 1) * limit
        return await self._repository.get_list(
            limit=limit,
            offset=offset,
            order_by=order_by,
            reverse=reverse,
        )

    async def create_one(self, data: UserCreate) -> User:
        data.email = data.email.lower()
        data.password = self._hasher.get_psw_hash(psw=data.password)

        user = User(**data.model_dump())
        return await self._repository.create_one(user=user)

    async def patch_one(self, user: User, data: UserPatch) -> User:
        if data.email:
            data.email = data.email.lower()
        if data.password:
            data.password = self._hasher.get_psw_hash(psw=data.password)

        for key, val in data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(user, key, val)

        return await self._repository.patch_one(user=user)
