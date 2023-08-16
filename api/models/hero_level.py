from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class HeroLevels(Base):
    """Model of hero levels."""

    __tablename__ = 'hero_levels'

    level_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    need_experience = Column(BigInteger)
    count_sentences = Column(Integer)
    count_games = Column(Integer)
    order = Column(Integer)

    users = relationship('Users', back_populates='hero_level')
    heroes_levels_history = relationship('UsersHeroLevelsHistory', back_populates='hero_level')
