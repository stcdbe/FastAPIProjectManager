from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()


PG_URL = (f'postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@'
          f'{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}')

REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
