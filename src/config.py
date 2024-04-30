from pathlib import Path

from pydantic import DirectoryPath, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool
    PORT: int
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    BASE_DIR: DirectoryPath = Path(__file__).parent.parent

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int

    _PG_URL: str = "postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB: str

    PG_USER_TEST: str
    PG_PASSWORD_TEST: str
    PG_HOST_TEST: str
    PG_PORT_TEST: str
    PG_DB_TEST: str

    EMAIL_SMTP_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_SENDER: EmailStr
    TEST_EMAIL_RECEIVER: EmailStr

    @property
    def PG_URL(self) -> str:
        return self._PG_URL.format(
            PG_USER=self.PG_USER,
            PG_PASSWORD=self.PG_PASSWORD,
            PG_HOST=self.PG_HOST,
            PG_PORT=self.PG_PORT,
            PG_DB=self.PG_DB,
        )

    @property
    def PG_URL_TEST(self) -> str:
        return self._PG_URL.format(
            PG_USER=self.PG_USER_TEST,
            PG_PASSWORD=self.PG_PASSWORD_TEST,
            PG_HOST=self.PG_HOST_TEST,
            PG_PORT=self.PG_PORT_TEST,
            PG_DB=self.PG_DB_TEST,
        )

    model_config = SettingsConfigDict(env_file="./.env", case_sensitive=True)


settings = Settings()
