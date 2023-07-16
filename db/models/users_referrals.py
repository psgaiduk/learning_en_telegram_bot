from sqlalchemy import BigInteger, Column, ForeignKey

from db.models.base import Base
from settings import settings


class UsersReferrals(Base):
    """Model of user."""

    if settings.environment == 'local':
        __tablename__ = '_local_users_referrals'
    else:
        __tablename__ = 'users_referrals'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    friend_telegram_id = Column(ForeignKey('users.telegram_id'))
