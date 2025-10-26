from dataclasses import asdict
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.data.models.task_model import TaskModel
from src.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.data.repositories.task.base import AbstractTaskRepository
from src.data.repositories.task.converters import convert_task_model_to_entity
from src.domain.task.entities import Task
from src.domain.task.exc import TaskInvalidDataError, TaskNotFoundError


class SQLAlchemyTaskRepository(AbstractTaskRepository, SQLAlchemyRepository):
    __slots__ = ("_session_factory",)

    async def get_list_by_project_guid(self, project_guid: UUID) -> list[Task]:
        stmt = select(TaskModel).where(TaskModel.project_guid == project_guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            task_model_seq = res.scalars().all()
            return [convert_task_model_to_entity(task_model) for task_model in task_model_seq]

    async def get_one_by_guid(self, guid: UUID) -> Task:
        stmt = select(TaskModel).where(TaskModel.guid == guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                task_model = res.scalars().one()
                return convert_task_model_to_entity(task_model)

        except NoResultFound as e:
            msg = f"Task {guid} not found"
            raise TaskNotFoundError(msg) from e

    async def create_one(self, task: Task) -> UUID:
        stmt = insert(TaskModel).values(asdict(task)).returning(TaskModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while adding task {task.title}: {e!r}"
            raise TaskInvalidDataError(msg) from e

    async def patch_one(self, task: Task) -> UUID:
        stmt = update(TaskModel).where(TaskModel.guid == task.guid).values(asdict(task)).returning(TaskModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while patching task {task.guid}: {e!r}"
            raise TaskInvalidDataError(msg) from e

    async def delete_one(self, task: Task) -> UUID:
        stmt = delete(TaskModel).where(TaskModel.guid == task.guid).returning(TaskModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while deleting task {task.guid}: {e!r}"
            raise TaskInvalidDataError(msg) from e
