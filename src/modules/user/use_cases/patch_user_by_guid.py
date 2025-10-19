from uuid import UUID

from src.modules.user.entities.user import UserPatchData
from src.modules.user.services.user_service import UserService


class PatchUserByGUIDUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(self, user_guid: UUID, user_patch_data: UserPatchData) -> UUID:
        user = await self._user_service.get_one_by_guid(user_guid)
        return await self._user_service.patch_one(user, user_patch_data)
