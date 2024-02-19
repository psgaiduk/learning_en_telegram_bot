from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship

from models.association_sentences_tenses import sentence_tenses_association
from database import Base


class Tenses(Base):
    """Model of tenses."""

    __tablename__ = 'tenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    short_description = Column(Text)
    full_description = Column(Text)
    image_telegram_id = Column(Text)

    sentences = relationship('BooksSentences', secondary=sentence_tenses_association, back_populates='tenses')
