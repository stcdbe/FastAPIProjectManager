from dataclasses import asdict
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import desc, insert, select, update

from src.common.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.modules.user.data.models.converters import convert_user_model_to_entity
from src.modules.user.data.models.user_model import UserModel
from src.modules.user.data.repositories.base import AbstractUserRepository
from src.modules.user.entities.user import User


class SQLAlchemyUserRepository(AbstractUserRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool = False,
    ) -> list[User]:
        stmt = select(UserModel).where(UserModel.is_deleted == False).offset(offset).limit(limit)  # noqa: E712

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self._session.execute(stmt)
        user_model_seq = res.scalars().all()
        return [convert_user_model_to_entity(user_model) for user_model in user_model_seq]

    async def get_one_by_guid(self, guid: UUID) -> User:
        stmt = select(UserModel).where(UserModel.guid == guid)

        res = await self._session.execute(stmt)
        user_model = res.scalars().one()
        return convert_user_model_to_entity(user_model)

    async def get_one_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.guid == username)

        res = await self._session.execute(stmt)
        user_model = res.scalars().one()
        return convert_user_model_to_entity(user_model)

    async def create_one(self, user: User) -> UUID:
        stmt = insert(UserModel).values(**asdict(user)).returning(UserModel.guid)

        # try:
        res = await self._session.execute(stmt)
        await self._session.commit()

        # except IntegrityError as exc:
        #     await self._session.rollback()
        #     msg = f"{exc.orig}"
        #     raise InvalidUserDataError(msg) from exc

        return res.scalars().one()

    async def patch_one(self, user: User) -> UUID:
        stmt = update(UserModel).where(UserModel.guid == user.guid).values(**asdict(user)).returning(UserModel.guid)

        # try:
        res = await self._session.execute(stmt)
        await self._session.commit()

        # except IntegrityError as exc:
        #     await self._session.rollback()
        #     msg = f"{exc.orig}"
        #     raise InvalidUserDataError(msg) from exc

        return res.scalars().one()

    async def delete_one(self, user: User) -> UUID:
        stmt = (
            update(UserModel).where(UserModel.guid == user.guid).values(is_deleted=True, deleted_at=datetime.now(UTC))
        )

        # try:
        res = await self._session.execute(stmt)
        await self._session.commit()

        # except IntegrityError as exc:
        #     await self._session.rollback()
        #     msg = f"{exc.orig}"
        #     raise InvalidUserDataError(msg) from exc

        return res.scalars().one()
