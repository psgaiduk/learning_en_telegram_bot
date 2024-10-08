from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from models.association_sentenses_words import sentence_word_association
from database import Base


class Words(Base):
    """Model of words."""

    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True, autoincrement=True)
    type_word_id = Column(ForeignKey("type_words.type_word_id"))
    word = Column(String(128))
    translation = Column(JSON)
    transcription = Column(String(128))
    part_of_speech = Column(String(64))

    type_word = relationship("TypeWords", back_populates="words", uselist=False)
    sentences = relationship("BooksSentences", secondary=sentence_word_association, back_populates="words")
    users_words_history = relationship("UsersWordsHistory", back_populates="word")
