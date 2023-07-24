from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class LevelsEn(Base):
    """Model of level of english."""

    __tablename__ = 'levels_en'

    level_en_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    order = Column(Integer)

    users = relationship('Users', back_populates='level_en')
    type_grammar_exercises = relationship('TypeGrammarExercises', back_populates='level_en')
    books = relationship('Books', back_populates='level_en')
