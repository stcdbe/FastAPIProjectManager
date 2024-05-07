from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.modules.project.exceptions import InvalidProjectDataError
from src.modules.project.models.entities import Project
from src.modules.project.repositories.base import AbstractProjectRepository


class SQLAlchemyProjectRepository(AbstractProjectRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool = False,
    ) -> list[Project]:
        stmt = select(Project).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self._session.execute(stmt)
        return list(res.scalars().all())

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> Project | None:
        stmt = select(Project).filter_by(**kwargs)

        if load_tasks:
            stmt = stmt.options(selectinload(Project.tasks))

        res = await self._session.execute(stmt)
        return res.scalars().first()

    async def create_one(self, project: Project) -> Project:
        try:
            self._session.add(project)
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            raise InvalidProjectDataError(message=f"{exc.orig}") from exc

        else:
            await self._session.refresh(project)
            return project

    async def patch_one(self, project: Project) -> Project:
        try:
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            raise InvalidProjectDataError(message=f"{exc.orig}") from exc

        else:
            await self._session.refresh(project)
            return project

    async def del_one(self, project: Project) -> None:
        await self._session.delete(project)
        await self._session.commit()
