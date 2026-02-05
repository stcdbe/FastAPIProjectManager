from datetime import datetime
from enum import StrEnum
from typing import Final
from uuid import UUID

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.util import immutabledict

_NAMING_CONVENTION: Final[immutabledict[str, str]] = immutabledict(
    {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


class PGForeignKeyOnDeleteOption(StrEnum):
    """
    ### NO ACTION
    This is the default behavior if you do not specify an option.
    It raises an error if any referencing rows still exist when the constraint is checked at the end of the transaction.

    ### RESTRICT
    This prevents the deletion of a referenced row if any referencing rows exist in the child table.
    The essential difference from NO ACTION is that RESTRICT does not allow the check to be deferred until later in the
    transaction.

    ### CASCADE
    When the referenced row in the parent table is deleted, all rows in the child table that reference it are
    automatically deleted as well.

    ### SET NULL
    When the referenced row in the parent table is deleted, the referencing columns in the child table are
    automatically set to NULL, provided that the referencing columns are not defined as NOT NULL.

    ### SET DEFAULT
    When the referenced row in the parent table is deleted, the referencing columns in the child table are
    automatically set to their default values, provided a default value is specified for those columns.
    """

    NO_ACTION = "NO ACTION"
    RESTRICT = "RESTRICT"
    CASCADE = "CASCADE"
    SET_NULL = "SET NULL"
    SET_DEFAULT = "SET DEFAULT"


class SQLAlchemyBaseModel(DeclarativeBase, AsyncAttrs):
    metadata = MetaData(naming_convention=_NAMING_CONVENTION)
    __abstract__ = True

    guid: Mapped[UUID] = mapped_column(primary_key=True)

    def __str__(self) -> str:
        return f"SQL Record <Table: {self.__tablename__!r}, GUID: {self.guid!r}>"

    def __repr__(self) -> str:
        return self.__str__()


class SQLAlchemyTimedBaseModel(SQLAlchemyBaseModel):
    __abstract__ = True
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
