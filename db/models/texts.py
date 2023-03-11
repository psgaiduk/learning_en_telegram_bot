from sqlalchemy import Column, Integer, Text

from db.models.base import Base


class Texts(Base):
    """Model of user."""
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    text_en = Column(Text)
    text_ru = Column(Text)
    text_fr = Column(Text)
    text_es = Column(Text)
    text_ge = Column(Text)


