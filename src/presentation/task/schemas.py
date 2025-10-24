from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class _TaskBaseScheme(BaseModel):
    title: Annotated[str, Field(min_length=5, max_length=256)]
    description: str
    is_completed: bool
    executor_guid: UUID4


class TaskCreateScheme(_TaskBaseScheme):
    pass


class TaskPatchScheme(TaskCreateScheme):
    title: Annotated[str | None, Field(min_length=5, max_length=256)]  # type: ignore
    description: str | None  # type: ignore
    is_completed: bool | None  # type: ignore
    executor_guid: UUID4 | None  # type: ignore


class TaskGetScheme(_TaskBaseScheme):
    guid: UUID4
    created_at: datetime
    updated_at: datetime
    project_guid: UUID4


class TaskListGetScheme(BaseModel):
    tasks: list[TaskGetScheme]
