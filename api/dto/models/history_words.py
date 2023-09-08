from datetime import datetime
from typing import Optional

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


class CreateHistoryWordModelDTO(BaseModel):
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


class GetHistoryWordModelDTO(BaseModel):
    """Get history word DTO."""

    word_id: Optional[int]
    is_known: Optional[bool]
    count_view_gte: Optional[int]
    count_view_lte: Optional[int]
    correct_answers_gte: Optional[int]
    correct_answers_lte: Optional[int]
    incorrect_answers_gte: Optional[int]
    incorrect_answers_lte: Optional[int]
    correct_answers_in_row_gte: Optional[int]
    correct_answers_in_row_lte: Optional[int]
    page: int = 1
    limit: int = 100
