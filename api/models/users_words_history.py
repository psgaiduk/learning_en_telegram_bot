from datetime import datetime

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class UsersWordsHistory(Base):
    """Model of user's words history."""

    __tablename__ = "users_words_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_user_id = Column(ForeignKey("telegram_users.telegram_id"))
    word_id = Column(ForeignKey("words.word_id"))
    is_known = Column(Boolean, default=False)
    count_view = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    correct_answers_in_row = Column(Integer, default=0)
    increase_factor = Column(Float, default=2.0)
    interval_repeat = Column(Integer, default=600)
    repeat_datetime = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users", back_populates="words_history", uselist=False)
    word = relationship("Words", back_populates="users_words_history", uselist=False)
