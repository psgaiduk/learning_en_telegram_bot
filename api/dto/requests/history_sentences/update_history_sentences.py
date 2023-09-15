from pydantic import BaseModel


class UpdateBooksSentencesDTO(BaseModel):
    """Update books sentences DTO."""

    telegram_id: int
    sentence_id: int
    is_read: bool
