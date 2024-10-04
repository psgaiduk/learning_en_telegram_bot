from datetime import datetime

from app import db


class UsersAchievementsHistory(db.Model):
    """Model of history user's achievements."""

    __tablename__ = "users_achievements_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey("users.telegram_id"))
    achievement_id = db.Column(db.ForeignKey("achievements.achievement_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Users", back_populates="achievements_history", uselist=False)
    achievement = db.relationship("Achievements", back_populates="users_achievements_history", uselist=False)
