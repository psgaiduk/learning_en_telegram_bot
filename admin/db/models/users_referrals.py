from app import db


class UsersReferrals(db.Model):
    """Model of user's referral."""

    __tablename__ = 'users_referrals'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    friend_telegram_id = db.Column(db.ForeignKey('users.telegram_id'))

    user = db.relationship('Users', back_populates='referrals', foreign_keys=[telegram_id], uselist=False)
    friend = db.relationship('Users', back_populates='friends', foreign_keys=[friend_telegram_id], uselist=False)
