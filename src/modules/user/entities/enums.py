from enum import StrEnum, auto


class UserGender(StrEnum):
    M = "M"
    F = "F"


class AuthTokenTyp(StrEnum):
    access = auto()
    refresh = auto()
