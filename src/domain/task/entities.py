from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Task:
    guid: UUID
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    is_completed: bool
    project_guid: UUID
    executor_guid: UUID


@dataclass(slots=True)
class TaskCreateData:
    title: str
    description: str
    is_completed: bool
    executor_guid: UUID


@dataclass(slots=True)
class TaskPatchData:
    title: str | None
    description: str | None
    is_completed: bool | None
    executor_guid: UUID | None
