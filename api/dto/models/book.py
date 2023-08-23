from pydantic import BaseModel

from dto.models.books_sentences import BooksSentencesModelDTO


class BooksModelDTO(BaseModel):
    """Books DTO."""

    book_id: int
    title: str
    level_en_id: int
    author: str
    books_sentences: list[BooksSentencesModelDTO]
