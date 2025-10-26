from uuid import UUID

from src.services.user_service import UserService


class DeleteUserByGUIDUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(self, guid: UUID) -> UUID:
        user = await self._user_service.get_one_by_guid(guid)
        return await self._user_service.soft_delete_one_by_guid(user)
