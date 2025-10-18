from src.modules.user.entities.user import User


class GetOneUserByUsernameUseCase:
    async def execute(self, username: str) -> User: ...
