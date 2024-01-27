from typing import Any

from sqlalchemy import select, desc
from sqlalchemy.exc import DBAPIError, DataError, InvalidRequestError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SQLASessionDep
from src.repository import AbstractRepository
from src.user.usermodels import UserDB


class UserRepository(AbstractRepository):
    session: AsyncSession

    def __init__(self, session: SQLASessionDep) -> None:
        self.session = session

    async def get_list(self,
                       limit: int,
                       offset: int,
                       ordering: str,
                       reverse: bool = False) -> list[UserDB]:
        stmt = (select(UserDB)
                .offset(offset)
                .limit(limit))
        if reverse:
            stmt = stmt.order_by(desc(ordering))
        else:
            stmt = stmt.order_by(ordering)
        return list((await self.session.execute(stmt)).scalars().all())

    async def get_one(self, **kwargs: Any) -> UserDB | None:
        stmt = select(UserDB).filter_by(**kwargs)
        try:
            return (await self.session.execute(stmt)).scalars().first()
        except (DBAPIError, DataError, InvalidRequestError):
            await self.session.rollback()

    async def create_one(self, user: UserDB) -> UserDB | None:
        try:
            self.session.add(user)
            await self.session.commit()
            return user
        except IntegrityError:
            await self.session.rollback()

    async def patch_one(self, user: UserDB) -> UserDB | None:
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
