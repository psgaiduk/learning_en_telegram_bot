from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersGamesHistory(Base):
    """Model of history user's games."""

    __tablename__ = 'users_games_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    game_id = Column(ForeignKey('games.game_id'))
    created_at = Column(DateTime, default=datetime.utcnow())
    count_questions = Column(Integer)
    correct_answers = Column(Integer)
    mistakes = Column(Integer)
    scores = Column(Integer)

    user = relationship('Users', back_populates='games', uselist=False)
    game = relationship('Games', back_populates='users_games_history', uselist=False)
