from logging import getLogger

from src.domain.user.entities import AuthToken
from src.domain.user.enums import AuthTokenTyp
from src.domain.user.exc import UserInvalidCredentialsError
from src.services.auth_service import AuthService
from src.services.hasher_service import HasherService
from src.services.user_service import UserService

logger = getLogger()


class GenerateUserTokenUseCase:
    __slots__ = ("_auth_service", "_hasher_service", "_user_service")

    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        hasher_service: HasherService,
    ) -> None:
        self._auth_service = auth_service
        self._user_service = user_service
        self._hasher_service = hasher_service

    async def execute(self, username: str, password: str) -> AuthToken:
        user = await self._user_service.get_one_by_username(username)

        if not self._hasher_service.verify_psw(password, user.password):
            logger.warning("Failed attempt to generate access token for username: %s", username)
            msg = "Invalid username or password"
            raise UserInvalidCredentialsError(msg)

        acess_token = self._auth_service.generate_token(user.guid)
        refresh_token = self._auth_service.generate_token(user.guid, token_typ=AuthTokenTyp.REFRESH)

        return AuthToken(
            access_token=acess_token,
            refresh_token=refresh_token,
            token_type="bearer",  # noqa: S106
        )
