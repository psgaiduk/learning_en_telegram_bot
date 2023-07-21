from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersAchievementsHistory(Base):
    """Model of history user's achievements."""

    __tablename__ = 'users_achievements_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    achievement_id = Column(ForeignKey('achievements.achievement_id'))
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship('Users', back_populates='achievements_history', uselist=False)
    achievement = relationship('Achievements', back_populates='users_achievements_history', uselist=False)
