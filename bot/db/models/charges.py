from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.models.base import Base


class Charges(Base):
    """Model of charges."""

    __tablename__ = 'charges'

    charge_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))

    users_charges_history = relationship('UsersChargesHistory', back_populates='charge')