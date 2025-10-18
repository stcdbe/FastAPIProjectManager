from src.modules.user.entities.user import User


class AuthenticateUserByTokenUseCase:
    async def execute(self) -> User: ...
