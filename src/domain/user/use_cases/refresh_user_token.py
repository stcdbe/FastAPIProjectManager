from src.domain.user.entities import AuthToken
from src.domain.user.enums import AuthTokenTyp
from src.services.auth_service import AuthService


class RefreshUserTokenUseCase:
    __slots__ = ("_auth_service",)

    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def execute(self, token: str) -> AuthToken:
        user_guid = self._auth_service.validate_token_and_extract_user_guid(token, AuthTokenTyp.REFRESH)
        access_token = self._auth_service.generate_token(user_guid)
        refresh_token = self._auth_service.generate_token(user_guid, AuthTokenTyp.REFRESH)
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",  # noqa: S106
        )
