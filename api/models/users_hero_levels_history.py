from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UsersHeroLevelsHistory(Base):
    """Model of history user's hero levels."""

    __tablename__ = 'users_hero_levels_history'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    hero_level_id = Column(ForeignKey('hero_levels.level_id'))
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship('Users', back_populates='hero_levels_history', uselist=False)
    hero_level = relationship('HeroLevels', back_populates='heroes_levels_history', uselist=False)
