from typing import Optional

from pydantic import BaseModel


class CreateBooksSentencesDTO(BaseModel):
    """Create books sentences DTO."""

    telegram_id: int
    sentence_id: int
    is_read: Optional[bool] = False
