from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersBooksSentencesHistory(Base):
    """Model of history user's books sentences."""

    __tablename__ = 'users_books_sentences_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    sentence_id = Column(ForeignKey('books_sentences.sentence_id'))
    check_words = Column(JSON, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship('Users', back_populates='books_sentences_history', uselist=False)
    sentence = relationship('BooksSentences', back_populates='users_books_sentences_history', uselist=False)
