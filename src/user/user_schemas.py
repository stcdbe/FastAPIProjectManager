from datetime import datetime
from typing import Annotated

from annotated_types import Ge, Le
from pydantic import EmailStr, StringConstraints, UUID4, Field

from src.schemas import BaseModel, AbstractPagination
from src.user.user_enums import Sex


class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50,
                                               pattern=r'^[a-z0-9_-]*$')]
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)]
    company: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    job_title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    fullname: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    age: Annotated[int, Ge(18), Le(99)] | None = None
    sex: Sex | None = None


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=10,
                                               max_length=72)]


class UserPatch(UserCreate):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=50,
                                               pattern=r'^[a-z0-9_-]*$')] | None = None
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=50)] | None = None
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=10,
                                               max_length=72)] | None = None


class UserGet(UserBase):
    id: UUID4
    join_date: datetime


class UserPagination(AbstractPagination):
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=5, gt=0, le=10)
    order_by: str = Field(default='username'),
    reverse: bool = Field(default=False)
