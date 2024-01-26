from typing import Any

from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, IntegrityError, InvalidRequestError
from asyncpg.exceptions import DataError

from src.user.usermodels import UserDB
from src.user.userschemas import UserCreate, UserPatch
from src.auth.authutils import Hasher


async def count_users_db(session: AsyncSession, **kwargs: Any) -> int:
    stmt = select(func.count('*')).select_from(UserDB).filter_by(**kwargs)
    return (await session.execute(stmt)).scalar()


async def get_user_db(session: AsyncSession, **kwargs: Any) -> UserDB | None:
    try:
        stmt = select(UserDB).filter_by(**kwargs)
        return (await session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError, InvalidRequestError):
        await session.rollback()


async def get_some_users_db(session: AsyncSession,
                            offset: int,
                            limit: int,
                            ordering: str,
                            reverse: bool = False) -> list[UserDB]:
    stmt = (select(UserDB)
            .offset(offset)
            .limit(limit))
    if reverse:
        stmt = stmt.order_by(desc(ordering))
    else:
        stmt = stmt.order_by(ordering)
    return list((await session.execute(stmt)).scalars().all())


async def create_user_db(session: AsyncSession, user_data: UserCreate) -> UserDB | None:
    user_data.email = user_data.email.lower()
    user_data.password = Hasher.get_psw_hash(psw=user_data.password)

    new_user = UserDB()
    for key, val in user_data.model_dump().items():
        setattr(new_user, key, val)

    try:
        session.add(new_user)
        await session.commit()
        return new_user
    except IntegrityError:
        await session.rollback()


async def patch_user_db(session: AsyncSession, user: UserDB, upd_user_data: UserPatch) -> UserDB | None:
    if upd_user_data.email:
        upd_user_data.email = upd_user_data.email.lower()
    if upd_user_data.password:
        upd_user_data.password = Hasher.get_psw_hash(psw=upd_user_data.password)

    for key, val in upd_user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, val)

    try:
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
