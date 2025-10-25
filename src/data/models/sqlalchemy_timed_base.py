from datetime import datetime

from sqlalchemy.orm import Mapped

from src.data.models.sqlalchemy_base import SQLAlchemyBaseModel


class SQLAlchemyTimedBaseModel(SQLAlchemyBaseModel):
    __abstract__ = True
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
