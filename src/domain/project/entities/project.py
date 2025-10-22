from dataclasses import dataclass
from datetime import date, datetime
from typing import Any
from uuid import UUID


@dataclass(slots=True)
class Project:
    guid: UUID
    title: str
    description: str
    tech_stack: tuple[str, ...]
    additional_metadata: dict[str, Any]
    start_date: date
    constraint_date: date
    creator_guid: UUID
    mentor_guid: UUID | None
    created_at: datetime
    updated_at: datetime
    # tasks: list["Task"] | None


@dataclass(slots=True)
class ProjectCreateData:
    title: str
    description: str
    tech_stack: tuple[str, ...]
    additional_metadata: dict[str, Any]
    start_date: date
    constraint_date: date
    mentor_guid: UUID | None


@dataclass(slots=True)
class ProjectPatchData:
    title: str | None
    description: str | None
    tech_stack: tuple[str, ...] | None
    additional_metadata: dict[str, Any] | None
    start_date: date | None
    constraint_date: date | None
    mentor_guid: UUID | None


@dataclass(slots=True)
class ProjectReportSendData:
    project_guid: UUID
    email: str
