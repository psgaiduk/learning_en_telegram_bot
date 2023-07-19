from datetime import datetime

from sqlalchemy import Column, ForeignKey, Date, DateTime, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersSubscribes(Base):
    """Model of user's subscribes."""

    __tablename__ = 'users_subscribes'

    id = Column(primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    subscribe_id = Column(ForeignKey('subscribes.subscribe_id'))
    date_start = Column(Date)
    date_end = Column(Date)
    income = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('Users', back_populates='subscribes')
    subscribe = relationship('Subscribes', back_populates='users_subscribes', uselist=False)
