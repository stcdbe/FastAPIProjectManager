from dataclasses import asdict
from uuid import UUID

from sqlalchemy import delete, desc, insert, select, update

# from sqlalchemy.orm import selectinload
from src.common.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.modules.project.data.models.project_model import ProjectModel
from src.modules.project.data.repositories.base import AbstractProjectRepository
from src.modules.project.entities.project import Project


class SQLAlchemyProjectRepository(AbstractProjectRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool,
    ) -> list[Project]:
        stmt = select(ProjectModel).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def get_one_by_guid(self, guid: UUID, with_tasks: bool = False) -> Project:
        stmt = select(ProjectModel).where(ProjectModel.guid == guid)

        # if with_tasks:
        #     stmt = stmt.options(selectinload(ProjectModel.tasks))

        async with self._get_session() as session:
            res = await session.execute(stmt)
            return res.scalars().one()

    async def get_one_by_title(self, title: str) -> Project:
        stmt = select(ProjectModel).where(ProjectModel.title.icontains(title))

        async with self._get_session() as session:
            res = await session.execute(stmt)
            return res.scalars().one()

    async def create_one(self, project: Project) -> UUID:
        stmt = insert(ProjectModel).values(**asdict(project)).returning(ProjectModel.guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()

        # except IntegrityError as exc:
        #     msg = f"{exc.orig}"
        #     raise InvalidProjectDataError(msg) from exc

    async def patch_one(self, project: Project) -> UUID:
        stmt = (
            update(ProjectModel)
            .where(ProjectModel.guid == project.guid)
            .values(**asdict(project))
            .returning(ProjectModel.guid)
        )

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()

    async def delete_one(self, project: Project) -> UUID:
        stmt = delete(ProjectModel).where(ProjectModel.guid == project.guid).returning(ProjectModel.guid)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalars().one()
