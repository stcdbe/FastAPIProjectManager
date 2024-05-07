from datetime import datetime, timedelta
from typing import Annotated

from pydantic import UUID4, Field, StringConstraints, conset, field_validator, model_validator

from src.core.presentation.schemas import AbstractPagination, AttrsBaseModel
from src.modules.task.views.schemas import TaskGet


class _ProjectBase(AttrsBaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=500)]
    tech_stack: conset(str, min_length=1, max_length=5)
    start_date: datetime
    constraint_date: datetime
    mentor_guid: UUID4 | None


class ProjectCreate(_ProjectBase):
    @field_validator("start_date", "constraint_date")
    @classmethod
    def validate_date_range(cls, v: datetime) -> datetime:
        v = v.replace(tzinfo=None)
        if v < datetime.utcnow() - timedelta(days=1):
            msg = "Project start_date or constraint_date cannot be in the past"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_projects_dates(self) -> "ProjectCreate":
        if self.start_date > self.constraint_date:
            msg = "Project start_date cannot be older than project constraint_date"
            raise ValueError(msg)
        return self


class ProjectPatch(ProjectCreate):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)] | None = None
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=500)] | None = None
    tech_stack: conset(str, min_length=1, max_length=5) | None = None
    start_date: datetime | None = None
    constraint_date: datetime | None = None
    mentor_guid: UUID4 | None = None


class ProjectGet(_ProjectBase):
    guid: UUID4
    creator_guid: UUID4
    created_at: datetime
    updated_at: datetime


class ProjectWithTasksGet(ProjectGet):
    tasks: list[TaskGet]


class ProjectPagination(AbstractPagination):
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=5, gt=0, le=10)
    order_by: str = Field(default="project_title")
    reverse: bool = Field(default=False)
