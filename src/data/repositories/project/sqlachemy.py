from dataclasses import asdict
from uuid import UUID

from sqlalchemy import delete, desc, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.data.models.project_model import ProjectModel
from src.data.repositories.project.base import AbstractProjectRepository
from src.data.repositories.project.converters import convert_project_model_to_entity
from src.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.domain.project.entities import Project
from src.domain.project.exc import ProjectInvalidDataError, ProjectNotFoundError


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
            project_models_seq = res.scalars().all()
            return [convert_project_model_to_entity(model) for model in project_models_seq]

    async def get_one_by_guid(self, guid: UUID) -> Project:
        stmt = select(ProjectModel).where(ProjectModel.guid == guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                project_model = res.scalars().one()
                return convert_project_model_to_entity(project_model)

        except NoResultFound as e:
            msg = f"Project {guid} not found"
            raise ProjectNotFoundError(msg) from e

    async def create_one(self, project: Project) -> UUID:
        stmt = insert(ProjectModel).values(asdict(project)).returning(ProjectModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while adding project: {e!r}"
            raise ProjectInvalidDataError(msg) from e

    async def patch_one(self, project: Project) -> UUID:
        stmt = (
            update(ProjectModel)
            .where(ProjectModel.guid == project.guid)
            .values(asdict(project))
            .returning(ProjectModel.guid)
        )

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while pathcing project: {e!r}"
            raise ProjectInvalidDataError(msg) from e

    async def delete_one(self, project: Project) -> UUID:
        stmt = delete(ProjectModel).where(ProjectModel.guid == project.guid).returning(ProjectModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while deleting project: {e!r}"
            raise ProjectInvalidDataError(msg) from e
