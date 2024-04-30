from abc import ABC

from pydantic import BaseModel, ConfigDict


class AttrsBaseModel(BaseModel, ABC):
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str


class AbstractPagination(BaseModel, ABC):
    page: int
    limit: int
    order_by: str
    reverse: bool
