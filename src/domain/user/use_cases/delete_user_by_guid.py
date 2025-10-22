from uuid import UUID

from src.services.user_service import UserService


class DeleteUserByGUIDUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(self, guid: UUID) -> UUID:
        user = await self._user_service.get_one_by_guid(guid)
        return await self._user_service.soft_delete_one_by_guid(user)
