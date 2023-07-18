from sqlalchemy import BigInteger, Column, ForeignKey, VARCHAR, Date, DateTime, Integer

from db.models.base import Base
from settings import settings


class UsersSubscribes(Base):
    """Model of user."""

    if settings.environment == 'local':
        __tablename__ = '_local_users_subscribes'
    else:
        __tablename__ = 'users_subscribes'

    id = Column(primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    subscribe_id = Column(ForeignKey('subscribes.subscribe_id'))
    date_start = Column(Date)
    date_end = Column(Date)
    income = Column(Integer)
    created_at = Column(DateTime)
