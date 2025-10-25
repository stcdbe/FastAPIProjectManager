from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

if TYPE_CHECKING:
    from src.data.models.project.project_model import ProjectModel
    from src.data.models.task.task_model import TaskModel


class UserModel(SQLAlchemyTimedBaseModel):
    __tablename__ = "user"
    # main data
    username: Mapped[str] = mapped_column(String(128), index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(64))
    second_name: Mapped[str | None] = mapped_column(String(64))
    gender: Mapped[str | None] = mapped_column(String(1))
    company: Mapped[str | None] = mapped_column(String(128))
    join_date: Mapped[date | None]
    job_title: Mapped[str | None] = mapped_column(String(128))
    date_of_birth: Mapped[date | None]
    is_deleted: Mapped[bool]
    deleted_at: Mapped[datetime | None]
    # relations
    created_projects: Mapped[list["ProjectModel"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
        foreign_keys="ProjectModel.creator_guid",
    )
    mentioned_projects: Mapped[list["ProjectModel"]] = relationship(
        back_populates="mentor",
        cascade="all, delete-orphan",
        foreign_keys="ProjectModel.mentor_guid",
    )
    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="executor",
        cascade="all, delete-orphan",
    )
