from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Final

import yaml
from pydantic import AmqpDsn, DirectoryPath, EmailStr, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENCODING: Final[str] = "utf-8"
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
_ENV_FILE: Final[Path] = _BASE_DIR / ".env"
_LOGGER_CONF_YAML_FILE: Final[Path] = _BASE_DIR / "logger.conf.yaml"
_TEMPLATES_DIR: Final[Path] = _BASE_DIR / "src" / "templates"


def _parse_log_config() -> dict[str, Any]:
    with _LOGGER_CONF_YAML_FILE.open(encoding=_ENCODING) as file:
        return yaml.safe_load(file)  # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        case_sensitive=True,
        env_file=_ENV_FILE,
        env_file_encoding=_ENCODING,
        extra="ignore",
    )

    LOG_CONFIG: Annotated[dict[str, Any], Field(default_factory=_parse_log_config)]

    DEBUG: Annotated[bool, Field(default=False)]
    TESTING: Annotated[bool, Field(default=False)]
    HOST: Annotated[str, Field(default="localhost")]
    PORT: Annotated[int, Field(default=8000)]
    DOCS_URL: Annotated[str | None, Field(default=None)]
    REDOC_URL: Annotated[str | None, Field(default=None)]

    BASE_DIR: Annotated[DirectoryPath, Field(default=_BASE_DIR)]
    TEMPLATES_DIR: Annotated[DirectoryPath, Field(default=_TEMPLATES_DIR)]

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: Annotated[str, Field(default="HS256")]
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int

    PG_URL: PostgresDsn
    PG_URL_TEST: PostgresDsn

    RMQ_URL: AmqpDsn

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_SENDER: EmailStr
    TEST_EMAIL_RECEIVER: EmailStr


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
