from app import db


class Achievements(db.Model):
    """Model of achievements."""

    __tablename__ = "achievements"

    achievement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    condition = db.Column(db.JSON)
    image_telegram_url = db.Column(db.Text)
    image_url = db.Column(db.Text)

    users_achievements_history = db.relationship("UsersAchievementsHistory", back_populates="achievement")
