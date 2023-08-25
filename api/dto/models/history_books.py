from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from dto.models.book import BooksModelDTO


class BooksHistoryModelDTO(BaseModel):
    """Books history DTO."""

    id: int
    telegram_user_id: int
    book_id: int
    start_read: Optional[datetime]
    end_read = Optional[datetime]
    book: BooksModelDTO
