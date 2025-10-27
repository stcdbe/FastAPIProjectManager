from logging import getLogger

from src.domain.user.entities import User
from src.services.user_service import UserService

logger = getLogger()


class GetUserListUseCase:
    __slots__ = ("_user_service",)

    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def execute(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]:
        logger.info("Getting user list with offset=%i and limit=%i", offset, limit)
        return await self._user_service.get_list(offset, limit, order_by, reverse)
