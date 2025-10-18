from enum import StrEnum


class UserGender(StrEnum):
    M = "M"
    F = "F"


class AuthTokenTyp(StrEnum):
    ACCESS = "A"
    REFRESH = "R"
