from sqlalchemy import BigInteger, Column, JSON, Integer

from db.models.base import Base
from settings import settings


class CurrentUserText(Base):
    """Model of current user text."""

    if settings.environment == 'local':
        __tablename__ = '_local_current_user_text'
    else:
        __tablename__ = 'current_user_text'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger)
    text_id = Column(Integer)
    next_sentences = Column(JSON)
    previous_sentences = Column(JSON)
