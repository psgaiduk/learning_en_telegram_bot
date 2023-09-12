from datetime import datetime

from pydantic import BaseModel


class HistoryWordModelDTO(BaseModel):
    """History word DTO."""

    id: int
    telegram_user_id: int
    type_word_id: int
    word_id: int
    word: str
    is_known: bool
    count_view: int
    correct_answers: int
    incorrect_answers: int
    correct_answers_in_row: int
    translation: dict
    created_at: datetime
    updated_at: datetime
