from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateHistoryWordDTO(BaseModel):
    """Create history word DTO."""

    telegram_user_id: int
    word_id: int
    is_known: Optional[bool]
    count_view: Optional[int]
    correct_answers: Optional[int]
    incorrect_answers: Optional[int]
    correct_answers_in_row: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
