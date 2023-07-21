from sqlalchemy import Column, String, Text, Integer, JSON
from sqlalchemy.orm import relationship

from db.models.base import Base


class Achievements(Base):
    """Model of achievements."""

    __tablename__ = 'achievements'

    achievement_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    condition = Column(JSON)
    image_telegram_url = Column(Text)
    image_url = Column(Text)

