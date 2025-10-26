from uuid import UUID

from src.domain.user.entities import UserPatchData
from src.services.user_service import UserService


class PatchUserByGUIDUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(self, user_guid: UUID, user_patch_data: UserPatchData) -> UUID:
        user = await self._user_service.get_one_by_guid(user_guid)
        return await self._user_service.patch_one(user, user_patch_data)
