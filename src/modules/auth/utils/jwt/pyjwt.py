from typing import Any

from jwt import DecodeError, InvalidTokenError, decode, encode

from src.config import get_settings
from src.modules.auth.exceptions import JWTDecodeError
from src.modules.auth.utils.jwt.base import AbstractJWTManager


class PyJWTManager(AbstractJWTManager):
    def encode_token(self, payload: dict[str, Any]) -> str:
        return encode(
            payload=payload,
            key=get_settings().JWT_SECRET_KEY,
            algorithm=get_settings().JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return decode(
                jwt=token,
                key=get_settings().JWT_SECRET_KEY,
                algorithms=(get_settings().JWT_ALGORITHM,),
            )
        except (DecodeError, InvalidTokenError) as exc:
            msg = "JWT decode error"
            raise JWTDecodeError(msg) from exc
