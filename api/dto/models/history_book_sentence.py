from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from dto.models.history_words import HistoryWordModelDTO


class HistoryBookSentenceModelDTO(BaseModel):
    """History book sentence DTO."""

    id: int
    book_id: int
    telegram_id: int
    sentence_id: int
    is_read: bool
    created_at: Optional[datetime]

    words: list[HistoryWordModelDTO]
