from sqlalchemy import Column, VARCHAR, Integer

from db.models.base import Base


class LevelsEn(Base):
    """Model of user."""

    __tablename__ = 'levels_en'

    level_en_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(64))
    order = Column(Integer)
