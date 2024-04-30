from typing import Annotated, Any

from fastapi import Depends

from src.modules.auth.utils.hasher import Hasher
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository
from src.modules.user.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.user.views.schemas import UserCreate, UserPagination, UserPatch


class UserService:
    _repository: AbstractUserRepository

    def __init__(self, repository: Annotated[AbstractUserRepository, Depends(SQLAlchemyUserRepository)]) -> None:
        self._repository = repository

    async def get_one(self, **kwargs: Any) -> User | None:
        return await self._repository.get_one(**kwargs)

    async def get_list(self, params: UserPagination) -> list[User]:
        offset = (params.page - 1) * params.limit
        return await self._repository.get_list(
            limit=params.limit,
            offset=offset,
            order_by=params.order_by,
            reverse=params.reverse,
        )

    async def create_one(self, data: UserCreate) -> User:
        data.email = data.email.lower()
        data.password = Hasher.get_psw_hash(psw=data.password)

        user = User(**data.model_dump())
        return await self._repository.create_one(user=user)

    async def patch_one(self, user: User, data: UserPatch) -> User:
        if data.email:
            data.email = data.email.lower()
        if data.password:
            data.password = Hasher.get_psw_hash(psw=data.password)

        for key, val in data.model_dump(exclude_none=True, exclude_unset=True).items():
            setattr(user, key, val)

        return await self._repository.patch_one(user=user)
