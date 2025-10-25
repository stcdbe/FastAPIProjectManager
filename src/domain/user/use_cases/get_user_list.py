from src.domain.user.entities import User
from src.services.user_service import UserService


class GetUserListUseCase:
    def __init__(self) -> None:
        self._user_service = UserService()

    async def execute(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]:
        return await self._user_service.get_list(offset, limit, order_by, reverse)
