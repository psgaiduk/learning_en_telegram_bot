from typing import Optional

from pydantic import BaseModel

from dto.models import HeroLevelsModelDTO, LevelsEnModelDTO, MainLanguageDTO


class TelegramUserDTO(BaseModel):
    """Telegram user DTO."""

    telegram_id: int
    level_en_id: Optional[int]
    main_language_id: int
    user_name: str = 'New client'
    experience: int = 0
    hero_level_id: int
    previous_stage: Optional[str] = None
    stage: Optional[str] = None
    main_language: Optional[MainLanguageDTO] = None
    level_en: Optional[LevelsEnModelDTO] = None
    hero_level: Optional[HeroLevelsModelDTO] = None
