from uuid import UUID

from sqlalchemy import desc, insert, select, update
from sqlalchemy.exc import IntegrityError

from src.common.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.modules.user.data.models.user_model import UserModel
from src.modules.user.data.repositories.base import AbstractUserRepository
from src.modules.user.entities.user import User
from src.modules.user.exceptions import InvalidUserDataError


class SQLAlchemyUserRepository(AbstractUserRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        limit: int,
        offset: int,
        order_by: str,
        reverse: bool = False,
    ) -> list[User]:
        stmt = select(UserModel).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self._session.execute(stmt)
        return list(res.scalars().all())

    async def get_one_by_guid(self, guid: UUID) -> User:
        stmt = select(UserModel).where(UserModel.guid == guid)

        res = await self._session.execute(stmt)
        return res.scalars().one()

    async def create_one(self, user: User) -> UUID:
        stmt = insert(UserModel).values().returning(UserModel.guid)

        try:
            res = await self._session.execute(stmt)
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            msg = f"{exc.orig}"
            raise InvalidUserDataError(msg) from exc

        return res.scalars().one()

    async def patch_one(self, user: User) -> UUID:
        stmt = update(UserModel).where().values().returning(UserModel.guid)

        try:
            res = await self._session.execute(stmt)
            await self._session.commit()

        except IntegrityError as exc:
            await self._session.rollback()
            msg = f"{exc.orig}"
            raise InvalidUserDataError(msg) from exc

        return res.scalars().one()
