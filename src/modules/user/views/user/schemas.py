from datetime import date, datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, EmailStr, Field

from src.modules.user.entities.enums import UserGender


class _UserBaseScheme(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=128, pattern=r"^[a-z0-9_-]*$")]
    email: EmailStr
    first_name: Annotated[str | None, Field(max_length=64)]
    second_name: Annotated[str | None, Field(max_length=64)]
    gender: UserGender | None
    company: Annotated[str | None, Field(max_length=128)]
    join_date: date | None
    job_title: Annotated[str | None, Field(max_length=128)]
    date_of_birth: date | None


class UserCreateScheme(_UserBaseScheme):
    password: Annotated[str, Field(min_length=8, max_length=72)]


class UserPatchScheme(_UserBaseScheme):
    username: Annotated[str | None, Field(min_length=5, max_length=128, pattern=r"^[a-z0-9_-]*$")]
    email: EmailStr | None
    password: Annotated[str | None, Field(min_length=8, max_length=72)]


class UserGetScheme(_UserBaseScheme):
    guid: UUID4
    created_at: datetime
    updated_at: datetime


class UserListGetScheme(BaseModel):
    users: list[UserGetScheme]
