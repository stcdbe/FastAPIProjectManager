from logging import getLogger

from src.modules.user.entities.auth_token import AuthToken
from src.modules.user.entities.enums import AuthTokenTyp
from src.modules.user.services.auth_service import AuthService
from src.modules.user.services.hasher_service import BcryptHasher
from src.modules.user.services.user_service import UserService

logger = getLogger()


class GenerateUserTokenUseCase:
    def __init__(self) -> None:
        self._auth_service = AuthService()
        self._orm_user_service = UserService()
        self._hasher = BcryptHasher()

    async def execute(self, username: str, password: str) -> AuthToken:
        user = await self._orm_user_service.get_one_by_username(username)

        if not self._hasher.verify_psw(password, user.password):
            raise ValueError("")

        acess_token = self._auth_service.generate_token(user.guid)
        refresh_token = self._auth_service.generate_token(user.guid, token_typ=AuthTokenTyp.REFRESH)

        logger.info("Generated access and refresh tokens for user %s", user.guid)

        return AuthToken(
            access_token=acess_token,
            refresh_token=refresh_token,
            token_type="Bearer",  # noqa: S106
        )
