from sqlalchemy import BigInteger, Column, VARCHAR, Integer, Boolean

from db.models.base import Base


class Subscribes(Base):
    """Model of user."""

    __tablename__ = 'subscribes'

    subscribe_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(32))
    count_days = Column(Integer)
    price = Column(Integer, nullable=True)
    currency = Column(VARCHAR(5))
    is_active = Column(Boolean, default=True)
