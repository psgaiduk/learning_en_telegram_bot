from datetime import datetime

from app import db


class UsersBooksSentencesHistory(db.Model):
    """Model of history user's books sentences."""

    __tablename__ = 'users_books_sentences_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    sentence_id = db.Column(db.ForeignKey('books_sentences.sentence_id'))
    check_words = db.Column(db.JSON, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship('Users', back_populates='books_sentences_history', uselist=False)
    sentence = db.relationship('BooksSentences', back_populates='users_books_sentences_history', uselist=False)
