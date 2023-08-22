from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class LevelsEn(Base):
    """Model of level of english."""

    __tablename__ = 'levels_en'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(64))
    description = Column(String(128))
    order = Column(Integer)

    users = relationship('Users', back_populates='level_en')
    # type_grammar_exercises = relationship('TypeGrammarExercises', back_populates='level_en')
    books = relationship('BooksModel', back_populates='level_en')