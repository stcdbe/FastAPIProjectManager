from typing import Annotated

from pydantic import UUID4, StringConstraints

from src.common.presentation.schemas import FromAttrsBaseModel, GUIDMixin, TimeMixin


class _TaskBase(FromAttrsBaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=250)]
    is_completed: bool = False
    executor_guid: UUID4


class TaskCreate(_TaskBase):
    pass


class TaskPatch(TaskCreate):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)] | None = None
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=250)] | None = None
    is_completed: bool | None = None
    executor_guid: UUID4 | None = None


class TaskGet(_TaskBase, GUIDMixin, TimeMixin):
    pass
