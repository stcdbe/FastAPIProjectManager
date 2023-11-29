from datetime import datetime
from typing import Annotated

from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, UUID4

from src.database.dbmodels import Sex


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=100)]
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=100)]
    company: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    job_title: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    fullname: Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)] | None = None
    age: Annotated[int, Ge(18), Le(99)] | None = 20
    sex: Sex | None = None


class UserCreate(User):
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=10,
                                               max_length=100)]


class UserPatch(UserCreate):
    username: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=5,
                                               max_length=100)] | None = None
    email: Annotated[EmailStr, StringConstraints(strip_whitespace=True,
                                                 min_length=5,
                                                 max_length=100)] | None = None
    password: Annotated[str, StringConstraints(strip_whitespace=True,
                                               min_length=10,
                                               max_length=100)] | None = None


class UserGet(User):
    join_date: datetime
    id: UUID4
