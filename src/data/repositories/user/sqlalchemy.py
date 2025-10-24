from dataclasses import asdict
from uuid import UUID

from sqlalchemy import desc, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.data.models.user.converters import convert_user_model_to_entity
from src.data.models.user.user_model import UserModel
from src.data.repositories.sqlalchemy_base import SQLAlchemyRepository
from src.data.repositories.user.base import AbstractUserRepository
from src.domain.user.entities.user import User
from src.domain.user.exc import UserCreateError, UserNotFoundError, UserPatchError


class SQLAlchemyUserRepository(AbstractUserRepository, SQLAlchemyRepository):
    async def get_list(
        self,
        offset: int,
        limit: int,
        order_by: str,
        reverse: bool,
    ) -> list[User]:
        stmt = select(UserModel).where(UserModel.is_deleted == False).offset(offset).limit(limit)  # noqa: E712

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        async with self._get_session() as session:
            res = await session.execute(stmt)
            user_model_seq = res.scalars().all()
            return [convert_user_model_to_entity(user_model) for user_model in user_model_seq]

    async def get_one_by_guid(self, guid: UUID) -> User:
        stmt = select(UserModel).where(UserModel.guid == guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                user_model = res.scalars().one()
                return convert_user_model_to_entity(user_model)

        except NoResultFound as e:
            msg = f"User {guid} not found"
            raise UserNotFoundError(msg) from e

    async def get_one_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                user_model = res.scalars().one()
                return convert_user_model_to_entity(user_model)

        except NoResultFound as e:
            msg = f"User {username} not found"
            raise UserNotFoundError(msg) from e

    async def create_one(self, user: User) -> UUID:
        stmt = insert(UserModel).values(**asdict(user)).returning(UserModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while adding user {user.username}: {e!r}"
            raise UserCreateError(msg) from e

    async def patch_one(self, user: User) -> UUID:
        stmt = update(UserModel).where(UserModel.guid == user.guid).values(**asdict(user)).returning(UserModel.guid)

        try:
            async with self._get_session() as session:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalars().one()

        except IntegrityError as e:
            msg = f"Error while patching user {user.guid}: {e!r}"
            raise UserPatchError(msg) from e
