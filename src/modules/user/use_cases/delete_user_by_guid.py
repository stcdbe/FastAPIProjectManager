from uuid import UUID

from src.modules.user.services.user_service import UserService


class DeleteUserByGUIDUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(self, guid: UUID) -> UUID:
        return await self._user_service.delete_one_by_guid(guid)
