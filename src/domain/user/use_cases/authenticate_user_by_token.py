from src.domain.user.entities.user import User
from src.services.auth_service import AuthService
from src.services.user_service import UserService


class AuthenticateUserByTokenUseCase:
    def __init__(self) -> None:
        self._auth_service = AuthService()
        self._user_service = UserService()

    async def execute(self, token: str) -> User:
        user_guid = self._auth_service.validate_token_and_extract_user_guid(token)
        return await self._user_service.get_one_by_guid(user_guid)
