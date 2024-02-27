from abc import ABC

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class AbstractPagination(BaseModel, ABC):
    page: int
    limit: int
    order_by: str
    reverse: bool
