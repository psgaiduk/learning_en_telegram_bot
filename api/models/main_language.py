from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class MainLanguages(Base):
    """Model of main languages."""

    __tablename__ = 'main_languages'

    main_language_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))

    users = relationship('Users', back_populates='main_language')
