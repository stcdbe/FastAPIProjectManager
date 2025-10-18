from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from src.config import get_settings
from src.modules.user.entities.enums import AuthTokenTyp


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
            msg = ""
            raise TypeError(msg) from e

        if token_typ != expected_token_typ:
            msg = ""
            raise TypeError(msg)

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
        token_payload = {"sub": str(user_guid), "token_typ": token_typ, "exp": exp}

        return jwt.encode(
            payload=token_payload,
            key=get_settings().JWT_SECRET_KEY,
            algorithm=get_settings().JWT_ALGORITHM,
        )
