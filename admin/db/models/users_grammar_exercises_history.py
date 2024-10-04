from datetime import datetime

from app import db


class UsersGrammarExercisesHistory(db.Model):
    """Model of history user's grammar exercises."""

    __tablename__ = "users_grammar_exercises_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey("users.telegram_id"))
    grammar_exercise_id = db.Column(db.ForeignKey("grammar_exercises.grammar_exercise_id"))
    is_answered = db.Column(db.Boolean, default=False)
    is_correct = db.Column(db.Boolean)
    scores = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Users", back_populates="grammar_exercises_history", uselist=False)
    grammar_exercise = db.relationship(
        "GrammarExercises",
        back_populates="users_grammar_exercises_history",
        uselist=False,
    )
