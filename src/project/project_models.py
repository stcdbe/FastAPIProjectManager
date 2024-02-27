from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey, false
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import TimedBaseModelDB

if TYPE_CHECKING:
    from src.user.user_models import UserDB


class ProjectDB(TimedBaseModelDB):
    __tablename__ = 'project'
    project_title: Mapped[str]
    project_description: Mapped[str]
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(item_type=String))
    start_date: Mapped[datetime]
    constraint_date: Mapped[datetime]
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['UserDB'] = relationship(back_populates='created_projects',
                                             foreign_keys=(creator_id,))
    mentor_id: Mapped[UUID | None] = mapped_column(ForeignKey('user.id'))
    mentor: Mapped['UserDB'] = relationship(back_populates='mentioned_projects',
                                            foreign_keys=(mentor_id,))
    tasks: Mapped[list['TaskDB']] = relationship(back_populates='project',
                                                 cascade='all, delete-orphan',
                                                 order_by='TaskDB.created_at.desc()')


class TaskDB(TimedBaseModelDB):
    __tablename__ = 'task'
    task_title: Mapped[str]
    task_description: Mapped[str]
    is_completed: Mapped[bool] = mapped_column(server_default=false(), default=False)
    project_id: Mapped[UUID] = mapped_column(ForeignKey('project.id'))
    project: Mapped['ProjectDB'] = relationship(back_populates='tasks')
    executor_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    executor: Mapped['UserDB'] = relationship(back_populates='tasks')
