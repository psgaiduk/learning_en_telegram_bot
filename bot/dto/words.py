from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WordDTOModel(BaseModel):
    """Model of word."""

    word_id: int
    word: str
    type_word_id: int
    transcription: str
    part_of_speech: str
    translation: Optional[dict[str, str]]
    is_known: bool
    count_view: int
    correct_answers: int
    incorrect_answers: int
    correct_answers_in_row: int
    increase_factor: float
    interval_repeat: int
    repeat_datetime: datetime
