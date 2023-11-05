from typing import Optional

from pydantic import BaseModel


class UpdateHistoryBooksSentencesDTO(BaseModel):
    """Update books sentences DTO."""

    id: int
    is_read: Optional[bool]
    check_words: Optional[list[int]]
