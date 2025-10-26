from src.domain.user.entities import User
from src.services.auth_service import AuthService
from src.services.user_service import UserService


class AuthenticateUserByTokenUseCase:
    __slots__ = ("_auth_service", "_user_service")

    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
    ) -> None:
        self._auth_service = auth_service
        self._user_service = user_service

    async def execute(self, token: str) -> User:
        user_guid = self._auth_service.validate_token_and_extract_user_guid(token)
        return await self._user_service.get_one_by_guid(user_guid)
