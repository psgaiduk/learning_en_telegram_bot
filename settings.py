from functools import lru_cache
from os import path

from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    openai_token: str = Field(..., env='OPEN_AI_TOKEN')
    path_to_database: str = path.join(path.dirname(__file__), 'database.db')
    telegram_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')

    class Config:
        """Config."""

        env_file = path.join(path.dirname(__file__), '.env')


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
