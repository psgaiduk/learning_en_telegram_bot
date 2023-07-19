from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class Games(Base):
    """Model of games."""

    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    is_active = Column(Boolean, default=True)

    history = relationship('UsersGamesHistory', back_populates='game')
