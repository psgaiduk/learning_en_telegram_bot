from pydantic import BaseModel


class TelegramUserDTO(BaseModel):
    """Telegram user DTO."""

    telegram_id: int
    level_en_id: int
    main_language_id: int
    user_name: str
    experience: int
    hero_level_id: int
    previous_stage: str
    stage: str
