from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.project.project_models import ProjectDB
from src.repositories import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    async def get_list(self,
                       limit: int,
                       offset: int,
                       order_by: str,
                       reverse: bool = False) -> list[ProjectDB]:
        stmt = select(ProjectDB).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_one(self, load_tasks: bool = False, **kwargs: Any) -> ProjectDB | None:
        stmt = select(ProjectDB).filter_by(**kwargs)

        if load_tasks:
            stmt = stmt.options(selectinload(ProjectDB.tasks))

        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def create_one(self, project: ProjectDB) -> ProjectDB:
        try:
            self.session.add(project)
            await self.session.commit()

        except IntegrityError as exc:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail=f'{exc.orig}')

        else:
            await self.session.refresh(project)
            return project

    async def patch_one(self, project: ProjectDB) -> ProjectDB:
        try:
            await self.session.commit()

        except IntegrityError as exc:
            await self.session.rollback()
            HTTPException(status_code=409, detail=f'{exc.orig}')

        else:
            await self.session.refresh(project)
            return project

    async def del_one(self, project: ProjectDB) -> None:
        await self.session.delete(project)
        await self.session.commit()
