from functools import lru_cache

from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Settings for postgres."""

    host: str = Field(..., env='POSTGRES_HOST')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    db_name: str = Field(..., env='POSTGRES_DB')

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}/{self.db_name}"


class MainSettings(BaseSettings):
    """All settings."""

    environment: str = Field(..., env='ENVIRONMENT')
    openai_token: str = Field(..., env='OPEN_AI_TOKEN')
    api_key: str = Field(..., env='API_KEY')

    postgres: PostgresSettings = PostgresSettings()



@lru_cache()
def get_settings() -> MainSettings:
    """Function for getting all settings."""
    return MainSettings()


settings = get_settings()
