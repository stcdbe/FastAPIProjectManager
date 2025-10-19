from datetime import UTC, datetime, timedelta
from logging import getLogger
from uuid import UUID

import jwt

from src.config import get_settings
from src.modules.user.entities.enums import AuthTokenTyp
from src.modules.user.exc import UserInvalidTokenError

logger = getLogger()


class AuthService:
    def validate_token_and_extract_user_guid(
        self,
        token: str,
        expected_token_typ: AuthTokenTyp = AuthTokenTyp.ACCESS,
    ) -> UUID:
        try:
            token_payload = jwt.decode(
                jwt=token,
                key=get_settings().JWT_SECRET_KEY,
                algorithms=(get_settings().JWT_ALGORITHM,),
            )
            user_guid = UUID(token_payload["sub"])
            token_typ = AuthTokenTyp(token_payload["typ"])
        except (jwt.PyJWTError, KeyError, ValueError) as e:
            logger.warning("Error while decoding token %s error: %s", token, e)
            msg = f"Error while decoding token {token}"
            raise UserInvalidTokenError(msg) from e

        if token_typ != expected_token_typ:
            logger.warning("Error while decoding token %s invalid token_typ %s", token, expected_token_typ)
            msg = f"Error while decoding token {token}"
            raise UserInvalidTokenError(msg)

        return user_guid

    def generate_token(
        self,
        user_guid: UUID,
        token_typ: AuthTokenTyp = AuthTokenTyp.ACCESS,
    ) -> str:
        if token_typ == AuthTokenTyp.ACCESS:
            delta = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRES)
        else:
            delta = timedelta(minutes=get_settings().REFRESH_TOKEN_EXPIRES)

        exp = datetime.now(UTC) + delta
        token_payload = {"sub": str(user_guid), "typ": token_typ, "exp": exp}

        return jwt.encode(
            payload=token_payload,
            key=get_settings().JWT_SECRET_KEY,
            algorithm=get_settings().JWT_ALGORITHM,
        )
