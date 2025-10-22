from logging import getLogger

from src.domain.user.entities.auth_token import AuthToken
from src.domain.user.entities.enums import AuthTokenTyp
from src.domain.user.exc import UserInvalidCredentialsError
from src.services.auth_service import AuthService
from src.services.hasher_service import Hasher
from src.services.user_service import UserService

logger = getLogger()


class GenerateUserTokenUseCase:
    def __init__(self) -> None:
        self._auth_service = AuthService()
        self._user_service = UserService()
        self._hasher = Hasher()

    async def execute(self, username: str, password: str) -> AuthToken:
        user = await self._user_service.get_one_by_username(username)

        if not self._hasher.verify_psw(password, user.password):
            logger.warning("Failed attempt to generate access token for username: %s", username)
            msg = "Invalid username or password"
            raise UserInvalidCredentialsError(msg)

        acess_token = self._auth_service.generate_token(user.guid)
        refresh_token = self._auth_service.generate_token(user.guid, token_typ=AuthTokenTyp.REFRESH)

        return AuthToken(
            access_token=acess_token,
            refresh_token=refresh_token,
            token_type="Bearer",  # noqa: S106
        )
