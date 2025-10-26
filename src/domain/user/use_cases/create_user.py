from uuid import UUID

from src.domain.user.entities import UserCreateData
from src.services.user_service import UserService


class CreateUserUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(self, user_create_data: UserCreateData) -> UUID:
        return await self._user_service.create_one(user_create_data)
