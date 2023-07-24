from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersReferrals(Base):
    """Model of user's referral."""

    __tablename__ = 'users_referrals'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    friend_telegram_id = Column(ForeignKey('users.telegram_id'))

    user = relationship('Users', back_populates='referrals', foreign_keys=[telegram_id], uselist=False)
    friend = relationship('Users', back_populates='friends', foreign_keys=[friend_telegram_id], uselist=False)
