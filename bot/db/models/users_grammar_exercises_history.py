from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersGrammarExercisesHistory(Base):
    """Model of history user's grammar exercises."""

    __tablename__ = 'users_grammar_exercises_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    grammar_exercise_id = Column(ForeignKey('grammar_exercises.grammar_exercise_id'))
    is_answered = Column(Boolean, default=False)
    is_correct = Column(Boolean)
    scores = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship('Users', back_populates='grammar_exercises_history', uselist=False)
    grammar_exercise = relationship('GrammarExercises', back_populates='users_grammar_exercises_history', uselist=False)
