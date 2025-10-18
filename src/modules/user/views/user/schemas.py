from datetime import datetime
from typing import Annotated

from annotated_types import Ge, Le
from pydantic import EmailStr, Field, StringConstraints

from src.common.presentation.schemas import AbstractPagination, FromAttrsBaseModel, GUIDMixin
from src.modules.user.models.enums import UserSex


class _UserBase(FromAttrsBaseModel):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=5,
            max_length=50,
            pattern=r"^[a-z0-9_-]*$",
        ),
    ]
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True, min_length=5, max_length=50)]
    company: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    job_title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    fullname: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    age: Annotated[int, Ge(18), Le(99)] | None = None
    sex: UserSex | None = None


class UserCreate(_UserBase):
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=72)]


class UserPatch(UserCreate):
    username: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                min_length=5,
                max_length=50,
                pattern=r"^[a-z0-9_-]*$",
            ),
        ]
        | None
    ) = None
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True, min_length=5, max_length=50)] | None = None
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=72)] | None = None


class UserGet(_UserBase, GUIDMixin):
    join_date: datetime


class UserPagination(AbstractPagination):
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=5, gt=0, le=10)
    order_by: str = Field(default="username")
    reverse: bool = Field(default=False)
