from pathlib import Path

from pydantic import DirectoryPath, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=True,
    )

    DEBUG: bool
    PORT: int
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    BASE_DIR: DirectoryPath = Path(__file__).parent.parent

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int

    PG_URL: PostgresDsn

    PG_URL_TEST: PostgresDsn

    EMAIL_SMTP_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_SENDER: EmailStr
    TEST_EMAIL_RECEIVER: EmailStr


settings = Settings()
