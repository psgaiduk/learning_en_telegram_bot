from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class TypeGrammarExercises(Base):
    """Model of type of grammar exercises."""

    __tablename__ = 'type_grammar_exercises'

    type_grammar_exercises_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    level_en_id = Column(ForeignKey('levels_en.level_en_id'))
    correct_scores = Column(Integer)
    incorrect_scores = Column(Integer)

    grammar_exercises = relationship('GrammarExercises', back_populates='type_grammar_exercise')
    level_en = relationship('LevelsEn', back_populates='type_grammar_exercises', uselist=False)
