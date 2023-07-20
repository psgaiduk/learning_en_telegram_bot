from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class Books(Base):
    """Model of books."""

    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    level_en_id = Column(ForeignKey('levels_en.level_en_id'))
    author = Column(String(128))
