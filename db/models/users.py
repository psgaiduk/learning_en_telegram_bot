from sqlalchemy import BigInteger, Column, Integer, String

from db.models.base import Base
from settings import settings


class Users(Base):
    """Model of user."""

    if settings.environment == 'local':
        __tablename__ = '_local_users'
    else:
        __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    level = Column(Integer)
    main_language = Column(String)
    learn_language = Column(String)
