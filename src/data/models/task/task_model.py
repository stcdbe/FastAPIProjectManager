from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

if TYPE_CHECKING:
    from src.data.models.project.project_model import ProjectModel
    from src.data.models.user.user_model import UserModel


class TaskModel(SQLAlchemyTimedBaseModel):
    __tablename__ = "task"
    # main data
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    is_completed: Mapped[bool]
    # foreign keys
    project_guid: Mapped[UUID] = mapped_column(ForeignKey("project.guid"))
    executor_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))
    # relations
    project: Mapped["ProjectModel"] = relationship(back_populates="tasks")
    executor: Mapped["UserModel"] = relationship(back_populates="tasks")
