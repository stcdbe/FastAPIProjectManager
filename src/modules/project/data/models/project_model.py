from datetime import date

# from typing import TYPE_CHECKING
from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

# , relationship
from src.common.data.models.sqlalchemy_timed_base import SQLAlchemyTimedBaseModel

# if TYPE_CHECKING:
# from src.modules.task.data.models.task_model import TaskModel
# from src.modules.user.data.models.user_model import UserModel


class ProjectModel(SQLAlchemyTimedBaseModel):
    __tablename__ = "project"

    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    tech_stack: Mapped[tuple[str, ...]] = mapped_column(ARRAY(item_type=String, as_tuple=True))
    additional_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB)
    start_date: Mapped[date]
    constraint_date: Mapped[date]
    creator_guid: Mapped[UUID] = mapped_column(ForeignKey("user.guid"))
    mentor_guid: Mapped[UUID | None] = mapped_column(ForeignKey("user.guid"))

    # creator: Mapped["UserModel"] = relationship(back_populates="created_projects", foreign_keys=(creator_guid,))
    # mentor: Mapped["UserModel"] = relationship(back_populates="mentioned_projects", foreign_keys=(mentor_guid,))
    # tasks: Mapped[list["TaskModel"]] = relationship(
    #     back_populates="project",
    #     cascade="all, delete-orphan",
    #     order_by="Task.created_at.desc()",
    # )
