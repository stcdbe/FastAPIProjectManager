from dataclasses import dataclass

from src.common.exc import BaseAppError


@dataclass(eq=False, frozen=True, slots=True)
class UserNotFoundError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class UserIsSoftDeletedError(UserNotFoundError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class UserCreateError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class UserPatchError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class UserInvalidTokenError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class UserInvalidCredentialsError(BaseAppError):
    pass
