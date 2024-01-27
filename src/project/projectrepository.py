from typing import Any

from sqlalchemy import select, desc
from sqlalchemy.exc import InvalidRequestError, DataError, DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dependencies import SQLASessionDep
from src.project.projectmodels import ProjectDB
from src.repository import AbstractRepository


class ProjectRepository(AbstractRepository):
    session: AsyncSession

    def __init__(self, session: SQLASessionDep) -> None:
        self.session = session

    async def get_list(self,
                       limit: int,
                       offset: int,
                       ordering: str,
                       reverse: bool = False) -> list[ProjectDB]:
        stmt = (select(ProjectDB)
                .offset(offset)
                .limit(limit))
        if reverse:
            stmt = stmt.order_by(desc(ordering))
        else:
            stmt = stmt.order_by(ordering)
        return list((await self.session.execute(stmt)).scalars().all())

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> ProjectDB | None:
        stmt = select(ProjectDB).filter_by(**kwargs)

        if load_tasks:
            stmt = stmt.options(selectinload(ProjectDB.tasks))

        try:
            return (await self.session.execute(stmt)).scalars().first()
        except (DBAPIError, DataError, InvalidRequestError):
            await self.session.rollback()

    async def create_one(self, project: ProjectDB) -> ProjectDB | None:
        try:
            self.session.add(project)
            await self.session.commit()
            return project
        except IntegrityError:
            await self.session.rollback()

    async def patch_one(self, project: ProjectDB) -> ProjectDB | None:
        try:
            await self.session.commit()
            await self.session.refresh(project)
            return project
        except IntegrityError:
            await self.session.rollback()

    async def del_one(self, project: ProjectDB) -> None:
        await self.session.delete(project)
        await self.session.commit()
