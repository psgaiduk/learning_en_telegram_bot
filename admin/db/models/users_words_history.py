from datetime import datetime

from app import db


class UsersWordsHistory(db.Model):
    """Model of user's words history."""

    __tablename__ = 'users_words_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    word_id = db.Column(db.ForeignKey('words.word_id'))
    is_known = db.Column(db.Boolean)
    count_view = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    incorrect_answers = db.Column(db.Integer, default=0)
    correct_answers_in_row = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Users', back_populates='words_history', uselist=False)
    word = db.relationship('Words', back_populates='users_words_history', uselist=False)
