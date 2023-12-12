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

    history_sentence_id: int
    sentence_id: int
    book_id: int
    text: str
    text_with_words: str
    translation: dict[str, str]

    words: list[HistoryWordModelForReadDTO]
