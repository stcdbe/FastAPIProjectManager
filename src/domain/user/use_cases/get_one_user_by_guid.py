from uuid import UUID

from src.domain.user.entities import User
from src.services.user_service import UserService


class GetOneUserByGUIDUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(self, guid: UUID) -> User:
        return await self._user_service.get_one_by_guid(guid)
