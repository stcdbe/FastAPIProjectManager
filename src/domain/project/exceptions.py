from dataclasses import dataclass

from src.common.exc import BaseAppError


@dataclass(eq=False, frozen=True, slots=True)
class InvalidProjectDataError(BaseAppError):
    pass
