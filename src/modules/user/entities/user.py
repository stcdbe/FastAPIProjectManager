from dataclasses import dataclass
from datetime import date

from src.modules.user.entities.enums import UserGender


@dataclass(slots=True)
class User:
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
