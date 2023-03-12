from sqlalchemy import BigInteger, Column, JSON, Integer

from db.models.base import Base


class CurrentUserText(Base):
    """Model of current user text."""
    __tablename__ = 'current_user_text'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    text_id = Column(Integer)
    next_sentences = Column(JSON)
    previous_sentences = Column(JSON)
