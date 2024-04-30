from dataclasses import dataclass


@dataclass
class AuthToken:
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
