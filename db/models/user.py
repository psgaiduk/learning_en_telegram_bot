from sqlalchemy import Column, Integer, String

from db.models.base import Base



class User(Base):
    """Model of user."""
    __tablename__ = 'user'

    telegram_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
