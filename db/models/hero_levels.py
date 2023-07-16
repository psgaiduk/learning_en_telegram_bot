from sqlalchemy import BigInteger, Column, VARCHAR, Integer

from db.models.base import Base


class HeroLevels(Base):
    """Model of hero levels."""

    __tablename__ = 'hero_levels'

    level_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(64))
    need_experience = Column(BigInteger)
    count_sentences = Column(Integer)
    count_games = Column(Integer)
    order = Column(Integer)
