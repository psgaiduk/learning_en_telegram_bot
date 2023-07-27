from datetime import datetime

from app import db


class UsersBooksHistory(db.Model):
    """Model of history user's books."""

    __tablename__ = 'users_books_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.ForeignKey('users.telegram_id'))
    book_id = db.Column(db.ForeignKey('books.book_id'))
    start_read = db.Column(db.DateTime, default=datetime.utcnow())
    end_read = db.Column(db.DateTime, nullable=True, default=None)

    user = db.relationship('Users', back_populates='books_history', uselist=False)
    book = db.relationship('Books', back_populates='users_books_history', uselist=False)
