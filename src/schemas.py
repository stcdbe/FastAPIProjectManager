from abc import ABC

from pydantic import BaseModel as _BaseModel, ConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message(_BaseModel):
    message: str


class AbstractPagination(_BaseModel, ABC):
    page: int
    limit: int
    order_by: str
    reverse: bool
