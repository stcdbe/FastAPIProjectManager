from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

if TYPE_CHECKING:
    from src.modules.task.data.models.task_model import Task
    from src.modules.user.data.models.user_model import User


class Project(SQLAlchemyTimedBaseModel):
    __tablename__ = "project"
    title: Mapped[str]
    description: Mapped[str]
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(item_type=String))
    start_date: Mapped[datetime]
    constraint_date: Mapped[datetime]
    creator_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))
    creator: Mapped["User"] = relationship(back_populates="created_projects", foreign_keys=(creator_guid,))
    mentor_guid: Mapped[UUID | None] = mapped_column(ForeignKey("user.guid"))
    mentor: Mapped["User"] = relationship(back_populates="mentioned_projects", foreign_keys=(mentor_guid,))
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Task.created_at.desc()",
    )
