from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int

    JWTSECRETKEY: str
    JWTALGORITHM: str
    ACCESSTOKENEXPIRESIN: int

    PGUSER: str
    PGPASSWORD: str
    PGHOST: str
    PGPORT: str
    PGDB: str

    PGUSERTEST: str
    PGPASSWORDTEST: str
    PGHOSTTEST: str
    PGPORTTEST: str
    PGDBTEST: str

    REDISHOST: str
    REDISPORT: str

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()

PGURL = (f'postgresql+asyncpg://{settings.PGUSER}:{settings.PGPASSWORD}@'
         f'{settings.PGHOST}:{settings.PGPORT}/{settings.PGDB}')

REDISURL = f'redis://{settings.REDISHOST}:{settings.REDISPORT}'
