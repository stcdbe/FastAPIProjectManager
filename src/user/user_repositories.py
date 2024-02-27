from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError

from src.repositories import SQLAlchemyRepository
from src.user.user_models import UserDB


class UserRepository(SQLAlchemyRepository):
    async def get_list(self,
                       limit: int,
                       offset: int,
                       order_by: str,
                       reverse: bool = False) -> list[UserDB]:
        stmt = select(UserDB).offset(offset).limit(limit)

        if reverse:
            stmt = stmt.order_by(desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_one(self, **kwargs: Any) -> UserDB | None:
        stmt = select(UserDB).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def create_one(self, user: UserDB) -> UserDB:
        try:
            self.session.add(user)
            await self.session.commit()

        except IntegrityError as exc:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail=f'{exc.orig}')

        else:
            await self.session.refresh(user)
            return user

    async def patch_one(self, user: UserDB) -> UserDB | None:
        try:
            await self.session.commit()

        except IntegrityError as exc:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail=f'{exc.orig}')

        else:
            await self.session.refresh(user)
            return user
