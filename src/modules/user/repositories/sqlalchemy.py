from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.modules.user.exceptions import InvalidUserDataError
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository


class SQLAlchemyUserRepository(AbstractUserRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool = False,
    ) -> list[User]:
        stmt = select(User).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self._session.execute(stmt)
        return list(res.scalars().all())

    async def get_one(self, **kwargs: Any) -> User | None:
        stmt = select(User).filter_by(**kwargs)

        res = await self._session.execute(stmt)
        return res.scalars().first()

    async def create_one(self, user: User) -> User:
        try:
            self._session.add(user)
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            raise InvalidUserDataError(message=f"{exc.orig}") from exc

        else:
            await self._session.refresh(user)
            return user

    async def patch_one(self, user: User) -> User:
        try:
            await self._session.flush()
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            raise InvalidUserDataError(message=f"{exc.orig}") from exc

        else:
            await self._session.refresh(user)
            return user
