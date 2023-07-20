from sqlalchemy import Column, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class GrammarExercises(Base):
    """Model of grammar exercises."""

    __tablename__ = 'grammar_exercises'

    grammar_exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    type_grammar_exercise_id = Column(ForeignKey('types_grammar_exercises.type_grammar_exercise_id'))
    text = Column(Text)

    type_grammar_exercise = relationship('TypeGrammarExercises', back_populates='grammar_exercises', uselist=False)
