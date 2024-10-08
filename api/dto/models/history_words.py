from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoryWordModelDTO(BaseModel):
    """History word DTO."""

    id: Optional[int]
    telegram_user_id: Optional[int]
    type_word_id: int
    word_id: int
    word: str
    transcription: Optional[str]
    part_of_speech: Optional[str]
    is_known: Optional[bool]
    count_view: Optional[int]
    correct_answers: Optional[int]
    incorrect_answers: Optional[int]
    correct_answers_in_row: Optional[int]
    increase_factor: Optional[float]
    interval_repeat: Optional[int]
    repeat_datetime: Optional[datetime]
    translation: Optional[dict]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class HistoryWordModelForReadDTO(BaseModel):
    """History word DTO for read."""

    type_word_id: int
    word_id: int
    word: str
    transcription: Optional[str]
    part_of_speech: str
    translation: Optional[dict]
    is_known: Optional[bool]
    count_view: Optional[int]
    correct_answers: Optional[int]
    incorrect_answers: Optional[int]
    correct_answers_in_row: Optional[int]
    increase_factor: Optional[float]
    interval_repeat: Optional[int]
    repeat_datetime: Optional[datetime]
