from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateHistoryWordDTO(BaseModel):
    """Update history word DTO."""

    telegram_user_id: int
    word_id: int
    is_known: Optional[bool]
    count_view: Optional[int]
    correct_answers: Optional[int]
    incorrect_answers: Optional[int]
    correct_answers_in_row: Optional[int]
    increase_factor: Optional[float]
    interval_repeat: Optional[int]
    repeat_datetime: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
