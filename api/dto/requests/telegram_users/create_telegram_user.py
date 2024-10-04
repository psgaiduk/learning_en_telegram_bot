from typing import Optional

from pydantic import BaseModel


class CreateTelegramUserDTO(BaseModel):
    """Create telegram user DTO."""

    telegram_id: int
    level_en_id: Optional[int]
    main_language_id: int
    user_name: str = "New client"
    experience: int = 0
    hero_level_id: int
    previous_stage: Optional[str] = None
    stage: Optional[str] = None
