from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from db.models.base import Base


class Subscribes(Base):
    """Model of subscribes."""

    __tablename__ = 'subscribes'

    subscribe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    count_days = Column(Integer)
    price = Column(Integer, nullable=True)
    currency = Column(String(5))
    is_active = Column(Boolean, default=True)

    users_subscribes = relationship('UsersSubscribes', back_populates='subscribe')
