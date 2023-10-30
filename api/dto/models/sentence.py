from pydantic import BaseModel

from dto.models.history_words import HistoryWordModelDTO


class SentenceModelDTO(BaseModel):
    """Sentence DTO."""

    sentence_id: int
    book_id: int
    text: str
    translation: dict[str, str]

    words: list[HistoryWordModelDTO]
