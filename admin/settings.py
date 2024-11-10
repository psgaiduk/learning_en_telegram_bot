from functools import lru_cache
from os import path

from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Settings for postgres."""

    host: str = Field(..., env="POSTGRES_HOST")
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    db_name: str = Field(..., env="POSTGRES_DB")


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env="ENVIRONMENT")
    nlp_token: str = Field(..., env="NLP_TOKEN")
    django_secret_key: str = Field(..., env="DJANGO_SECRET_KEY")
    debug: bool = Field(..., env="DEBUG")
    sentry_dsn: str = Field(..., env="SENTRY_DSN_DJANGO")
    ai_token: str = Field(..., env="OPEN_AI_TOKEN")
    hosts: str = Field(..., env="ALLOWED_HOSTS")

    postgres: PostgresSettings = PostgresSettings()


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
