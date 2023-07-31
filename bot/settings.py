from functools import lru_cache
from os import path

from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Settings for postgres."""

    host: str = Field(..., env='POSTGRES_HOST')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    db_name: str = Field(..., env='POSTGRES_DB')

    class Config:
        """Config."""

        env_file = path.join(path.dirname(__file__), '../.env')


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    openai_token: str = Field(..., env='OPEN_AI_TOKEN')
    path_to_database: str = path.join(path.dirname(__file__), 'database.db')
    telegram_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    nlp_token: str = Field(..., env='NLP_TOKEN')
    translate_word_token: str = Field(..., env='TRANSLATE_WORD_TOKEN')

    postgres: PostgresSettings = PostgresSettings()

    class Config:
        """Config."""

        env_file = path.join(path.dirname(__file__), '../.env')


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
