from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, text, ForeignKey, false
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModelDB
if TYPE_CHECKING:
    from src.user.usermodels import UserDB


class ProjectDB(BaseModelDB):
    __tablename__ = 'project'
    project_title: Mapped[str]
    project_description: Mapped[str]
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(item_type=String))
    start_date: Mapped[datetime]
    constraint_date: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow,
                                                 onupdate=datetime.utcnow)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['UserDB'] = relationship(back_populates='created_projects',
                                             foreign_keys=[creator_id])
    mentor_id: Mapped[UUID | None] = mapped_column(ForeignKey('user.id'))
    mentor: Mapped['UserDB'] = relationship(back_populates='mentioned_projects',
                                            foreign_keys=[mentor_id])
    tasks: Mapped[list['TaskDB']] = relationship(back_populates='project',
                                                 cascade='all, delete-orphan',
                                                 order_by='TaskDB.created_at.desc()')


class TaskDB(BaseModelDB):
    __tablename__ = 'task'
    task_title: Mapped[str]
    task_description: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(server_default=false(), default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow,
                                                 onupdate=datetime.utcnow)
    project: Mapped['ProjectDB'] = relationship(back_populates='tasks')
    project_id: Mapped[UUID] = mapped_column(ForeignKey('project.id'))
    executor: Mapped['UserDB'] = relationship(back_populates='tasks')
    executor_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
