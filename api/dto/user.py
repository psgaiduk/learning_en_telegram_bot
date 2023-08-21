from typing import Optional

from pydantic import BaseModel


class TelegramUserDTO(BaseModel):
    """Telegram user DTO."""

    telegram_id: int
    level_en_id: str
    main_language_id: str
    user_name: str = 'New client'
    experience: int = 0
    hero_level_id: int
    previous_stage: Optional[str]
    stage: Optional[str]
