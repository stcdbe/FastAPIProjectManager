from dataclasses import dataclass

from src.common.exc import BaseAppError


@dataclass(eq=False, frozen=True, slots=True)
class TaskNotFoundError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class TaskInvalidDataError(BaseAppError):
    pass
