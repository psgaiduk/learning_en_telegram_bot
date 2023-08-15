from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class BooksModel(Base):
    """Model of books."""

    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    level_en_id = Column(ForeignKey('levels_en.level_en_id'))
    author = Column(String(128))

    level_en = relationship('LevelsEn', back_populates='books', uselist=False)
    # users_books_history = db.relationship('UsersBooksHistory', back_populates='book', uselist=False)
    books_sentences = relationship('BooksSentences', back_populates='book')
