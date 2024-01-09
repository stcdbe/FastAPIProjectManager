from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql.expression import false
from sqlalchemy.dialects.postgresql import ARRAY

from src.database.enums import Sex


class BaseModelDB(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)

    def __repr__(self) -> str:
        return str(self.id)


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


class ProjectDB(BaseModelDB):
    __tablename__ = 'project'
    project_title: Mapped[str]
    project_description: Mapped[str]
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(item_type=String))
    start_date: Mapped[datetime]
    constraint_date: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow)
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
    project: Mapped['ProjectDB'] = relationship(back_populates='tasks')
    project_id: Mapped[UUID] = mapped_column(ForeignKey('project.id'))
    executor: Mapped['UserDB'] = relationship(back_populates='tasks')
    executor_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
