from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class UsersBooksHistory(Base):
    """Model of history user's books."""

    __tablename__ = "users_books_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_user_id = Column(ForeignKey("telegram_users.telegram_id"))
    book_id = Column(ForeignKey("books.book_id"))
    start_read = Column(DateTime, default=datetime.utcnow)
    end_read = Column(DateTime, nullable=True, default=None)

    user = relationship("Users", back_populates="books_history", uselist=False)
    book = relationship("BooksModel", back_populates="users_books_history", uselist=False)
