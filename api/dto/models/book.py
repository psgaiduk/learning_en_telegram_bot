from pydantic import BaseModel

from dto.models import BooksSentencesModelDTO


class BooksModelDTO(BaseModel):
    """Books DTO."""

    book_id: int
    title: str
    level_en_id: int
    author: str
    books_sentences: BooksSentencesModelDTO
