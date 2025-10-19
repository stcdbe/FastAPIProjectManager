from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

if TYPE_CHECKING:
    from src.modules.project.data.models.project_model import ProjectModel
    from src.modules.user.data.models.user_model import UserModel


class TaskModel(SQLAlchemyTimedBaseModel):
    __tablename__ = "task"
    title: Mapped[str]
    description: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)
    project_guid: Mapped[UUID] = mapped_column(ForeignKey("project.guid"))
    project: Mapped["ProjectModel"] = relationship(back_populates="tasks")
    executor_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))
    executor: Mapped["UserModel"] = relationship(back_populates="tasks")
