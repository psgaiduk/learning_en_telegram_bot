from sqlalchemy import Column, Integer, String

from db.models.base import Base


class Users(Base):
    """Model of user."""
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Integer)
