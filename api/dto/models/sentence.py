from pydantic import BaseModel

from dto.models.history_words import HistoryWordModelDTO, HistoryWordModelForReadDTO


class SentenceModelDTO(BaseModel):
    """Sentence DTO."""

    sentence_id: int
    book_id: int
    text: str
    translation: dict[str, str]

    words: list[HistoryWordModelDTO]


class SentenceModelForReadDTO(BaseModel):
    """Sentence DTO for read api."""

    sentence_id: int
    book_id: int
    text: str
    translation: dict[str, str]

    words: list[HistoryWordModelForReadDTO]