from enum import StrEnum, auto


class AuthTokenTyp(StrEnum):
    access = auto()
    refresh = auto()
