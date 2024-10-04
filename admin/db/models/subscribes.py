from app import db


class Subscribes(db.Model):
    """Model of subscribes."""

    __tablename__ = "subscribes"

    subscribe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    count_days = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(5))
    is_active = db.Column(db.Boolean, default=True)

    users_subscribes = db.relationship("UsersSubscribes", back_populates="subscribe")
