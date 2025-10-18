from src.modules.user.entities.user import User


class GetUserListUseCase:
    async def execute(self) -> list[User]: ...
