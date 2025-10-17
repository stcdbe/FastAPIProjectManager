from typing import Final
from uuid import UUID

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

_NAMING_CONVENTION: Final[dict[str, str]] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class SQLAlchemyBaseModel(DeclarativeBase, AsyncAttrs):
    metadata = MetaData(naming_convention=_NAMING_CONVENTION)
    __abstract__ = True

    guid: Mapped[UUID] = mapped_column(primary_key=True)

    def __str__(self) -> str:
        return f"SQL Record (Table: {self.__tablename__!r} GUID:{self.guid})"

    def __repr__(self) -> str:
        return self.__str__()
