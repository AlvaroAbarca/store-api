from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import (
    AnyHttpUrl,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class Environment(StrEnum):
    dev = "dev"
    prod = "prod"


class Paths:
    # coffee_api_ck
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / "app"
    EMAIL_TEMPLATES_DIR: Path = BASE_DIR / "emails"
    LOGIN_PATH: str = "/auth/login"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = "dev"
    SECRET_KEY: str = "SECRET_KEY"
    DEBUG: bool = False
    AUTH_TOKEN_LIFETIME_SECONDS: int = 3600 * 24 * 7
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"  # type:ignore
    SENTRY_DSN: HttpUrl | None = None
    PAGINATION_PER_PAGE: int = 20

    REDIS_URL: RedisDsn = "redis://localhost:6379/0"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_URI: str

    SES_ACCESS_KEY: str | None = None
    SES_SECRET_KEY: str | None = None
    SES_REGION: str | None = None
    DEFAULT_FROM_EMAIL: EmailStr = ""
    DEFAULT_FROM_NAME: str | None = None
    EMAILS_ENABLED: bool = False

    @field_validator("EMAILS_ENABLED")
    def get_emails_enabled(cls, _: bool, values: dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("DEFAULT_FROM_EMAIL")
        )

    FIRST_SUPERUSER_EMAIL: EmailStr = 'test@test.com'
    FIRST_SUPERUSER_PASSWORD: str = 'test'

    # class Config:
    #     env_file = ".env"


settings = Settings()
