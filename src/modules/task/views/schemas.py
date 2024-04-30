from datetime import datetime
from typing import Annotated

from pydantic import UUID4, StringConstraints

from src.core.presentation.schemas import AttrsBaseModel


class _TaskBase(AttrsBaseModel):
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


class TaskGet(TaskCreate):
    guid: UUID4
    created_at: datetime
    updated_at: datetime
