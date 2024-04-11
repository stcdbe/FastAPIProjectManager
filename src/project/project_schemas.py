from datetime import datetime, timedelta
from typing import Annotated

from pydantic import StringConstraints, conset, field_validator, UUID4, model_validator, Field

from src.schemas import BaseModel, AbstractPagination


class TaskBase(BaseModel):
    task_title: Annotated[str, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=100)]
    task_description: Annotated[str, StringConstraints(strip_whitespace=True,
                                                       min_length=5,
                                                       max_length=250)]
    is_completed: bool = False
    executor_id: UUID4


class TaskCreate(TaskBase):
    pass


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
    updated_at: datetime


class ProjectBase(BaseModel):
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


class ProjectCreate(ProjectBase):
    @field_validator('start_date', 'constraint_date')
    @classmethod
    def validate_date_range(cls, v: datetime) -> datetime:
        v = v.replace(tzinfo=None)
        if v < datetime.utcnow() - timedelta(days=1):
            raise ValueError('Project start_date or constraint_date cannot be in the past')
        return v

    @model_validator(mode='after')
    def validate_projects_dates(self) -> 'ProjectCreate':
        if self.start_date > self.constraint_date:
            raise ValueError('Project start_date cannot be older than project constraint_date')
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


class ProjectGet(ProjectBase):
    id: UUID4
    creator_id: UUID4
    created_at: datetime
    updated_at: datetime


class ProjectWithTasksGet(ProjectGet):
    tasks: list[TaskGet]


class ProjectPagination(AbstractPagination):
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=5, gt=0, le=10)
    order_by: str = Field(default='project_title'),
    reverse: bool = Field(default=False)
