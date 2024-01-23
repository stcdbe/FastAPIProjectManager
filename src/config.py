from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool
    PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int

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

    REDIS_HOST: str
    REDIS_PORT: str

    EMAIL_SMTP_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_SENDER: EmailStr
    TEST_EMAIL_RECEIVER: EmailStr

    @property
    def PG_URL(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'

    @property
    def PG_URL_TEST(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER_TEST}:{self.PG_PASSWORD_TEST}@{self.PG_HOST_TEST}:{self.PG_PORT_TEST}/{self.PG_DB_TEST}'

    @property
    def REDIS_URL(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()
