from datetime import datetime

from app import db


class UsersSubscribes(db.Model):
    """Model of user's subscribes."""

    __tablename__ = "users_subscribes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey("users.telegram_id"))
    subscribe_id = db.Column(db.ForeignKey("subscribes.subscribe_id"))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    income = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Users", back_populates="subscribes")
    subscribe = db.relationship("Subscribes", back_populates="users_subscribes", uselist=False)
