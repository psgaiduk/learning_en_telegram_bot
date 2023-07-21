from sqlalchemy import Column, ForeignKey, String, Integer, JSON
from sqlalchemy.orm import relationship

from db.models.base import Base


class Words(Base):
    """Model of words."""

    __tablename__ = 'words'

    word_id = Column(Integer, primary_key=True, autoincrement=True)
    type_word_id = Column(ForeignKey('type_words.type_word_id'))
    word = Column(String(128))
    translation = Column(JSON)

    type_word = relationship('TypeWords', back_populates='words', uselist=False)
    users_words_history = relationship('UsersWordsHistory', back_populates='word')
