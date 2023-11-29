from datetime import datetime, timedelta
from typing import Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict, conset, field_validator, UUID4, model_validator


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_title: Annotated[str, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=100)]
    task_description: Annotated[str, StringConstraints(strip_whitespace=True,
                                                       min_length=5,
                                                       max_length=250)]
    is_completed: bool
    executor_id: UUID4


class TaskPatch(TaskCreate):
    task_title: Annotated[str, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=100)] | None = None
    task_description: Annotated[str, StringConstraints(strip_whitespace=True,
                                                       min_length=5,
                                                       max_length=250)] | None = None
    is_completed: bool | None = None
    executor_id: UUID4 | None = None


class TaskGet(TaskCreate):
    id: UUID4
    created_at: datetime


class Project(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    project_title: Annotated[str, StringConstraints(strip_whitespace=True,
                                                    min_length=5,
                                                    max_length=100)]
    project_description: Annotated[str, StringConstraints(strip_whitespace=True,
                                                          min_length=5,
                                                          max_length=500)]
    tech_stack: conset(str, min_length=1, max_length=5)
    start_date: datetime
    constraint_date: datetime
    mentor_id: UUID4 | None


class ProjectCreate(Project):
    @field_validator('start_date', 'constraint_date')
    @classmethod
    def validate_date_range(cls, v: datetime) -> datetime:
        date = v.replace(tzinfo=None)
        if date < datetime.utcnow() - timedelta(days=1):
            raise ValueError('Project dates cannot be in the past')
        return date

    @model_validator(mode='after')
    def validate_projects_dates(self):
        if self.start_date > self.constraint_date:
            raise ValueError('start_date cannot be older than constraint_date')
        return self


class ProjectPatch(ProjectCreate):
    project_title: Annotated[str, StringConstraints(strip_whitespace=True,
                                                    min_length=5,
                                                    max_length=100)] | None = None
    project_description: Annotated[str, StringConstraints(strip_whitespace=True,
                                                          min_length=5,
                                                          max_length=500)] | None = None
    tech_stack: conset(str, min_length=1, max_length=5) | None = None
    start_date: datetime | None = None
    constraint_date: datetime | None = None
    mentor_id: UUID4 | None = None


class ProjectGet(Project):
    id: UUID4
    creator_id: UUID4
    created_at: datetime


class ProjectWithTasksGet(ProjectGet):
    tasks: list[TaskGet] | list[None]
