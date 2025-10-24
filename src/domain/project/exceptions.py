from dataclasses import dataclass

from src.common.exc import BaseAppError


@dataclass(eq=False, frozen=True, slots=True)
class ProjectNotFoundError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class ProjectCreateError(BaseAppError):
    pass


@dataclass(eq=False, frozen=True, slots=True)
class ProjectPatchError(BaseAppError):
    pass
