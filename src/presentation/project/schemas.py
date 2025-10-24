from datetime import UTC, date, datetime, timedelta
from typing import Annotated, Any, Self

from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator, model_validator


class _ProjectBaseScheme(BaseModel):
    title: Annotated[str, Field(max_length=256)]
    description: str
    tech_stack: Annotated[set[str], Field(min_length=1, max_length=100)]
    additional_metadata: dict[str, Any]
    start_date: date
    constraint_date: date
    mentor_guid: UUID4 | None


class ProjectCreateScheme(_ProjectBaseScheme):
    @field_validator("start_date", "constraint_date")
    @classmethod
    def validate_date_range(cls, v: date) -> date:
        if v < datetime.now(UTC).date() - timedelta(days=1):
            msg = "Project start_date or constraint_date cannot be in the past"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_projects_dates(self) -> Self:
        if self.start_date > self.constraint_date:
            msg = "Project start_date cannot be older than project constraint_date"
            raise ValueError(msg)
        return self


class ProjectPatchScheme(ProjectCreateScheme):
    title: Annotated[str, Field(max_length=256)] | None  # type: ignore
    description: str | None  # type: ignore
    tech_stack: Annotated[set[str], Field(min_length=1, max_length=100)] | None  # type: ignore
    start_date: date | None  # type: ignore
    constraint_date: date | None  # type: ignore
    mentor_guid: UUID4 | None


class ProjectGetScheme(_ProjectBaseScheme):
    guid: UUID4
    creator_guid: UUID4
    created_at: datetime
    updated_at: datetime


# class ProjectWithTasksGetScheme(ProjectGetScheme):
#     tasks: list[TaskGet]


class ProjectListGetScheme(BaseModel):
    projects: list[ProjectGetScheme]


class ProjectReportSendDataScheme(BaseModel):
    project_guid: UUID4
    email: EmailStr
