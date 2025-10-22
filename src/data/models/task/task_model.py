# from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# , relationship
from src.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

# if TYPE_CHECKING:
#     from src.data.models.project.project_model import ProjectModel
#     from src.data.models.user.user_model import UserModel


class TaskModel(SQLAlchemyTimedBaseModel):
    __tablename__ = "task"
    title: Mapped[str]
    description: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)
    project_guid: Mapped[UUID] = mapped_column(ForeignKey("project.guid"))
    executor_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))

    # project: Mapped["ProjectModel"] = relationship(back_populates="tasks")
    # executor: Mapped["UserModel"] = relationship(back_populates="tasks")
