from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models.base import SQLAlchemyBaseModel
from src.modules.user.models.enums import UserSex

if TYPE_CHECKING:
    from src.modules.project.models.entities import Project
    from src.modules.task.models.entities import Task


class User(SQLAlchemyBaseModel):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    company: Mapped[str | None]
    job_title: Mapped[str | None]
    fullname: Mapped[str | None]
    age: Mapped[int | None]
    sex: Mapped[UserSex | None]
    join_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_projects: Mapped[list["Project"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
        foreign_keys="Project.creator_guid",
    )
    mentioned_projects: Mapped[list["Project"]] = relationship(
        back_populates="mentor",
        cascade="all, delete-orphan",
        foreign_keys="Project.mentor_guid",
    )
    tasks: Mapped[list["Task"]] = relationship(back_populates="executor", cascade="all, delete-orphan")
