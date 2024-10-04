from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class TypeWords(Base):
    """Model of type of words."""

    __tablename__ = "type_words"

    type_word_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))

    words = relationship("Words", back_populates="type_word")
