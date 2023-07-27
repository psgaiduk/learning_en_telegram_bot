from datetime import datetime

from app import db


class UsersChargesHistory(db.Model):
    """Model of history user's charges."""

    __tablename__ = 'users_charges_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    charge_id = db.Column(db.ForeignKey('charges.charge_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    experience = db.Column(db.Integer)

    user = db.relationship('Users', back_populates='charges_history', uselist=False)
    charge = db.relationship('Charges', back_populates='users_charges_history', uselist=False)
