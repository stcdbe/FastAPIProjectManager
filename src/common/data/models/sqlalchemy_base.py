from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SQLAlchemyBaseModel(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    guid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)

    def __repr__(self) -> str:
        return f"table: {self.__tablename__} id: {self.guid}"
