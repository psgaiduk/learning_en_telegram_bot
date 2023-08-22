from typing import Optional

from pydantic import BaseModel

from dto import MainLanguageDTO


class TelegramUserDTO(BaseModel):
    """Telegram user DTO."""

    telegram_id: int
    level_en_id: int
    main_language_id: int
    user_name: str = 'New client'
    experience: int = 0
    hero_level_id: int
    previous_stage: Optional[str]
    stage: Optional[str]
    main_language: Optional[MainLanguageDTO]


class UpdateTelegramUserDTO(TelegramUserDTO):
    """Update telegram user DTO for patch."""
    telegram_id: Optional[int]
    level_en_id: Optional[int]
    main_language_id: Optional[int]
    user_name: Optional[str]
    experience: Optional[int]
    hero_level_id: Optional[int]
