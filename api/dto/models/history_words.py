from datetime import datetime

from pydantic import BaseModel


class HistoryWordModelDTO(BaseModel):
    """History word DTO."""

    id: int
    telegram_id: int
    word_id: int
    is_known: bool
    count_view: int
    correct_answers: int
    incorrect_answers: int
    correct_answers_in_row: int
    created_at: datetime
    updated_at: datetime
