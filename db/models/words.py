from sqlalchemy import Column, Integer, String

from db.models.base import Base


class Words(Base):
    """Model of user."""
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    words_en = Column(String)
    words_ru = Column(String)
    words_fr = Column(String)
    words_es = Column(String)
    words_ge = Column(String)



