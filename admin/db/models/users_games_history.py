from datetime import datetime

from app import db


class UsersGamesHistory(db.Model):
    """Model of history user's games."""

    __tablename__ = "users_games_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey("users.telegram_id"))
    game_id = db.Column(db.ForeignKey("games.game_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    count_questions = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    mistakes = db.Column(db.Integer)
    scores = db.Column(db.Integer)

    user = db.relationship("Users", back_populates="games_history", uselist=False)
    game = db.relationship("Games", back_populates="history", uselist=False)
