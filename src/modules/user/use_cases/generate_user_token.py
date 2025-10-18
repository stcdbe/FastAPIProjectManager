from src.modules.user.entities.auth_token import AuthToken


class GenerateUserTokenUseCase:
    async def execute(self, username: str, password: str) -> AuthToken: ...
