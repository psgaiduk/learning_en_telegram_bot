from pydantic import BaseModel


class SentenceDTO(BaseModel):
    """Sentence DTO."""

    text: str
    index: int
