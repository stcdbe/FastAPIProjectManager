from uuid import UUID

from src.modules.user.entities.user import UserCreateData
from src.modules.user.services.user_service import UserService


class CreateUserUseCase:
    def __init__(self) -> None:
        self._orm_user_service = UserService()

    async def execute(self, user_create_data: UserCreateData) -> UUID:
        return await self._orm_user_service.create_one(user_create_data)
