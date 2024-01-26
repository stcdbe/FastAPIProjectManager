from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.project.projectmodels import ProjectDB, TaskDB
from src.user.userenums import Sex
from src.models import BaseModelDB
if TYPE_CHECKING:
    from src.project.projectmodels import ProjectDB, TaskDB


class UserDB(BaseModelDB):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    join_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                default=datetime.utcnow)
    company: Mapped[str | None]
    job_title: Mapped[str | None]
    fullname: Mapped[str | None]
    age: Mapped[int | None]
    sex: Mapped[Sex | None]
    created_projects: Mapped[list['ProjectDB']] = relationship(back_populates='creator',
                                                               cascade='all, delete-orphan',
                                                               foreign_keys='ProjectDB.creator_id')
    mentioned_projects: Mapped[list['ProjectDB']] = relationship(back_populates='mentor',
                                                                 cascade='all, delete-orphan',
                                                                 foreign_keys='ProjectDB.mentor_id')
    tasks: Mapped[list['TaskDB']] = relationship(back_populates='executor',
                                                 cascade='all, delete-orphan')
