from dataclasses import dataclass

from src.common.exceptions.base import BaseAppError


@dataclass(eq=False, frozen=True, slots=True)
class InvalidAuthDataError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class JWTDecodeError(BaseAppError):
    pass
