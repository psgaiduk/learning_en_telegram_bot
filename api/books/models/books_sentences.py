from sqlalchemy import BigInteger, Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class BooksSentences(Base):
    """Model of books sentences."""

    __tablename__ = 'books_sentences'

    sentence_id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(ForeignKey('books.book_id'))
    order = Column(Integer)
    text = Column(JSON)
    translation = Column(JSON)
    words = Column(JSON)

    book = relationship('Books', back_populates='books_sentences', uselist=False)
    # users_books_sentences_history = db.relationship('UsersBooksSentencesHistory', back_populates='sentence')
