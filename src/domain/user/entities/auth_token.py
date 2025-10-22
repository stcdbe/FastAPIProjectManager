from dataclasses import dataclass


@dataclass(slots=True)
class AuthToken:
    access_token: str
    refresh_token: str | None
    token_type: str
