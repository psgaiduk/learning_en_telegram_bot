from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey

from db.models.base import Base


class UsersText(Base):
    __tablename__ = 'users_texts'

    id = Column(Integer, index=True, primary_key=True)
    date = Column(Integer)
    language = Column(String)
    user_telegram_id = Column(ForeignKey('users.telegram_id'))
    text_id = Column(ForeignKey('texts.id'))
