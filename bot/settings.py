from functools import lru_cache

from pydantic import BaseSettings, Field


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    telegram_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    api_url: str = Field(..., env='URL_API')
    api_token: str = Field(..., env='API_KEY')
    bot_name: str = Field(..., env='BOT_NAME')

    @property
    def api_headers(self) -> dict:
        return {'X-API-Key': self.api_token}


@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
