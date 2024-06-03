from abc import ABC
from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class FromAttrsBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GUIDMixin(FromAttrsBaseModel):
    guid: UUID4


class TimeMixin(FromAttrsBaseModel):
    created_at: datetime
    updated_at: datetime


class Message(BaseModel):
    message: str


class AbstractPagination(BaseModel, ABC):
    page: int
    limit: int
    order_by: str
    reverse: bool
