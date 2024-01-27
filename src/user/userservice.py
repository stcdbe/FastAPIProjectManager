from typing import Any, Annotated

from fastapi import Depends

from src.auth.authutils import Hasher
from src.user.usermodels import UserDB
from src.user.userrepository import UserRepository
from src.user.userschemas import UserCreate, UserPatch


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    async def get_one(self, **kwargs: Any) -> UserDB | None:
        return await self.user_repository.get_one(**kwargs)

    async def get_list(self, params: dict[str, Any]) -> list[UserDB]:
        offset = (params['page'] - 1) * params['limit']
        return await self.user_repository.get_list(limit=params['limit'],
                                                   offset=offset,
                                                   ordering=params['ordering'],
                                                   reverse=params['reverse'])

    async def create_one(self, user_data: UserCreate) -> UserDB | None:
        user_data.email = user_data.email.lower()
        user_data.password = Hasher.get_psw_hash(psw=user_data.password)

        new_user = UserDB()
        for key, val in user_data.model_dump().items():
            setattr(new_user, key, val)

        return await self.user_repository.create_one(new_user)

    async def patch_one(self, user: UserDB, upd_user_data: UserPatch) -> UserDB | None:
        if upd_user_data.email:
            upd_user_data.email = upd_user_data.email.lower()
        if upd_user_data.password:
            upd_user_data.password = Hasher.get_psw_hash(psw=upd_user_data.password)

        for key, val in upd_user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, val)

        return await self.user_repository.patch_one(user)
