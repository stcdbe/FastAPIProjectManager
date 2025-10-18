from typing import Annotated

from pydantic import BaseModel, Field


class AuthTokenScheme(BaseModel):
    access_token: str
    refresh_token: Annotated[str | None, Field(default=None)]
    token_type: Annotated[str, Field(default="Bearer")]
