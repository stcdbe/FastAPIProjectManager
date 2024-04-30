from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import TimedSQLAlchemyBaseModel

if TYPE_CHECKING:
    from src.modules.project.models.entities import Project
    from src.modules.user.models.entities import User


class Task(TimedSQLAlchemyBaseModel):
    __tablename__ = "task"
    title: Mapped[str]
    description: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(default=False)
    project_guid: Mapped[UUID] = mapped_column(ForeignKey("project.guid"))
    project: Mapped["Project"] = relationship(back_populates="tasks")
    executor_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))
    executor: Mapped["User"] = relationship(back_populates="tasks")
