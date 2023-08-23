from pydantic import BaseModel

from dto.models import WordsModelDTO


class BooksSentencesModelDTO(BaseModel):
    """Books sentences DTO."""

    sentence_id: int
    book_id: int
    order: int
    text: dict
    translation: dict
    words: list[WordsModelDTO]
