from sqlalchemy import Column, String

from db.models.base import Base


class Word(Base):
    __tablename__ = 'words'

    english = Column(String, primary_key=True)
    russian = Column(String)
