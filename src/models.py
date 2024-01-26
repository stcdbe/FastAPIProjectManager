from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModelDB(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)

    def __repr__(self) -> str:
        return f'{self.__tablename__}: {self.id}'
