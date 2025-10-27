from logging import getLogger
from uuid import UUID

from src.services.user_service import UserService

logger = getLogger()


class DeleteUserByGUIDUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(self, user_guid: UUID) -> UUID:
        logger.info("Deleting user %s", user_guid)
        user = await self._user_service.get_one_by_guid(user_guid)
        return await self._user_service.soft_delete_one_by_guid(user)
