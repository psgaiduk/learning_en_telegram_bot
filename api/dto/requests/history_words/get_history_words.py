from typing import Optional

from pydantic import BaseModel


class GetHistoryWordsDTO(BaseModel):
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
