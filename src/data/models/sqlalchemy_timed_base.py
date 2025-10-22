from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.sqlalchemy_base import SQLAlchemyBaseModel


class SQLAlchemyTimedBaseModel(SQLAlchemyBaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
