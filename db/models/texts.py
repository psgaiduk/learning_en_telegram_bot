from sqlalchemy import Column, Integer, Text

from db.models.base import Base


class Texts(Base):
    """Model of user."""
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    text = Column(Text)
