from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.modules.user.entities.enums import UserGender


@dataclass(slots=True)
class User:
    guid: UUID
    username: str
    email: str
    password: str
    first_name: str | None
    second_name: str | None
    gender: UserGender | None
    company: str | None
    join_date: date | None
    job_title: str | None
    date_of_birth: date | None
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(guid={self.guid})"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(slots=True)
class UserCreateData:
    username: str
    email: str
    password: str
    first_name: str | None
    second_name: str | None
    gender: UserGender | None
    company: str | None
    join_date: date | None
    job_title: str | None
    date_of_birth: date | None


@dataclass(slots=True)
class UserPatchData:
    username: str | None
    email: str | None
    password: str | None
    first_name: str | None
    second_name: str | None
    gender: UserGender | None
    company: str | None
    join_date: date | None
    job_title: str | None
    date_of_birth: date | None
