from dataclasses import asdict
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from src.data.models.task.task_model import TaskModel
from src.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.data.repositories.task.base import AbstractTaskRepository
from src.domain.task.entities.task import Task, TaskCreateData, TaskPatchData


class SQLAlchemyTaskRepository(AbstractTaskRepository, SQLAlchemyRepository):
    async def get_list(self) -> list[Task]:
        stmt = select(TaskModel).where()

        async with self._get_session() as session:
            res = await session.execute(stmt)
            task_model_seq = res.scalars().all()

    async def create_one(self, task_create_data: TaskCreateData) -> UUID:
        stmt = insert(TaskModel).values(asdict(task_create_data)).returning(TaskModel.guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()

    async def patch_one(self, guid: UUID, task_patch_data: TaskPatchData) -> UUID:
        stmt = update(TaskModel).where(TaskModel.guid == guid).values(asdict(task_patch_data)).returning(TaskModel.guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()

    async def delete_one(self, guid: UUID) -> UUID:
        stmt = delete(TaskModel).where(TaskModel.guid == guid).returning(TaskModel.guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()
