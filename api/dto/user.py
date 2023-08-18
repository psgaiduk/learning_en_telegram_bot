from typing import Optional

from pydantic import BaseModel


class TelegramUserDTO(BaseModel):
    """Telegram user DTO."""

    telegram_id: int
    level_en: Optional[str]
    main_language: Optional[str]
    user_name: Optional[str]
    experience: int = 0
    hero_level: Optional[int]
    previous_stage: Optional[str]
    stage: Optional[str]
