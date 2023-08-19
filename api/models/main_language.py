from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class MainLanguages(Base):
    """Model of main languages."""

    __tablename__ = 'main_languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    description = Column(String(128))

    users = relationship('Users', back_populates='main_language')


class MainLanguagesModelDTO(BaseModel):
    """DTO of main languages."""

    id: int
    title: str
    description: str
