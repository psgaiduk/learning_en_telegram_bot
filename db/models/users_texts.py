from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey

from db.models.base import Base
from settings import settings


class UsersText(Base):
    """Model of user's text."""

    if settings.environment == 'local':
        __tablename__ = '0_local_users_texts'
    else:
        __tablename__ = 'users_texts'

    id = Column(Integer, index=True, primary_key=True)
    date = Column(Integer)
    language = Column(String)
    user_telegram_id = Column(ForeignKey('users.telegram_id'))
    text_id = Column(ForeignKey('texts.id'))
