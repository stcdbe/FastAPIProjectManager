from uuid import UUID

from src.domain.user.entities.user import User
from src.services.user_service import UserService


class GetOneUserByGUIDUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(self, guid: UUID) -> User:
        return await self._user_service.get_one_by_guid(guid)
