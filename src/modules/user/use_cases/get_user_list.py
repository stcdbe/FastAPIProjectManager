from src.modules.user.entities.user import User
from src.modules.user.services.user_service import UserService


class GetUserListUseCase:
    def __init__(self) -> None:
        self._orm_user_service = UserService()

    async def execute(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]:
        return await self._orm_user_service.get_list(offset, limit, order_by, reverse)
