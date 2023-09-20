from functools import lru_cache

from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    telegram_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
