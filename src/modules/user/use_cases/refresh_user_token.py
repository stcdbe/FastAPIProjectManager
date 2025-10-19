from src.modules.user.entities.auth_token import AuthToken
from src.modules.user.entities.enums import AuthTokenTyp
from src.modules.user.services.auth_service import AuthService
from src.modules.user.services.user_service import UserService


class RefreshUserTokenUseCase:
    def __init__(self) -> None:
        self._auth_service = AuthService()
        self._user_service = UserService()

    async def execute(self, token: str) -> AuthToken:
        user_guid = self._auth_service.validate_token_and_extract_user_guid(token)
        user = await self._user_service.get_one_by_guid(user_guid)

        access_token = self._auth_service.generate_token(user.guid)
        refresh_token = self._auth_service.generate_token(user.guid, AuthTokenTyp.REFRESH)
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",  # noqa: S106
        )
