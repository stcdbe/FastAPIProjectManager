from uuid import UUID

from src.modules.user.entities.user import User
from src.modules.user.services.user_service import UserService


class GetOneUserByGUIDUseCase:
    def __init__(self) -> None:
        self._orm_user_service = UserService()

    async def execute(self, guid: UUID) -> User:
        return await self._orm_user_service.get_one_by_guid(guid)
