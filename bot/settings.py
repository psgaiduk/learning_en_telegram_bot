from functools import lru_cache

from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    telegram_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    url_api: str = Field('api:8001', env='URL_API')


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
