from functools import lru_cache
from os import path

from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Settings for postgres."""

    host: str = Field(..., env='POSTGRES_HOST')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    db_name: str = Field(..., env='POSTGRES_DB')


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    openai_token: str = Field(..., env='OPEN_AI_TOKEN')

    postgres: PostgresSettings = PostgresSettings()



@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
