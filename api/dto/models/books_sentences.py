from pydantic import BaseModel

from dto.models.words import WordsModelDTO


class BooksSentencesModelDTO(BaseModel):
    """Books sentences DTO."""

    sentence_id: int
    book_id: int
    order: int
    text: str
    translation: dict
    words: list[WordsModelDTO]
