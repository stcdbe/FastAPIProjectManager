from src.common.exceptions.base import BaseAppError


class InvalidAuthDataError(BaseAppError):
    pass


class JWTDecodeError(BaseAppError):
    pass
