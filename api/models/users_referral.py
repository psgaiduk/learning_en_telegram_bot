from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class UsersReferrals(Base):
    """Model of referral user."""
    
    __tablename__ = 'users_referrals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('telegram_users.telegram_id'))
    friend_telegram_id = Column(ForeignKey('telegram_users.telegram_id'))

    user = relationship('Users', back_populates='referrals', foreign_keys=[telegram_id], uselist=False)
    friend = relationship('Users', back_populates='friends', foreign_keys=[friend_telegram_id], uselist=False)
