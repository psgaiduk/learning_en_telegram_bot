from typing import Optional

from pydantic import BaseModel


class UpdateTelegramUserDTO(BaseModel):
    """Update telegram user DTO for patch."""

    telegram_id: int
    level_en_id: Optional[int]
    main_language_id: Optional[int]
    user_name: Optional[str]
    experience: Optional[int]
    hero_level_id: Optional[int]
    previous_stage: Optional[str]
    stage: Optional[str]
