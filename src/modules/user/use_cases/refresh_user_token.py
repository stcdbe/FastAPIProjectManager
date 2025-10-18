from src.modules.user.entities.auth_token import AuthToken


class RefreshUserTokenUseCase:
    async def execute(self, token: str) -> AuthToken: ...
