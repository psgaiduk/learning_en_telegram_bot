from sqlalchemy import BigInteger, Column, Integer, String

from db.models.base import Base


class Users(Base):
    """Model of user."""
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    level = Column(Integer)
    main_language = Column(String)
    learn_language = Column(String)
