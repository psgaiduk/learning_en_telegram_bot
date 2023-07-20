from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class UsersChargesHistory(Base):
    """Model of history user's charges."""

    __tablename__ = 'users_charges_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(ForeignKey('users.telegram_id'))
    charge_id = Column(ForeignKey('charges.charge_id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    experience = Column(Integer)

    user = relationship('Users', back_populates='games', uselist=False)
    charge = relationship('Charges', back_populates='users_charges_history', uselist=False)
