from app import db


class Charges(db.Model):
    """Model of charges."""

    __tablename__ = 'charges'

    charge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))

    users_charges_history = db.relationship('UsersChargesHistory', back_populates='charge')