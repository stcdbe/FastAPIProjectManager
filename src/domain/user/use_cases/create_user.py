from uuid import UUID

from src.domain.user.entities import UserCreateData
from src.services.user_service import UserService


class CreateUserUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(self, user_create_data: UserCreateData) -> UUID:
        return await self._user_service.create_one(user_create_data)
