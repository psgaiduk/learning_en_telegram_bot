from db import db


class Books(db.Model):
    """Model of books."""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    level_en_id = db.Column(db.ForeignKey('levels_en.level_en_id'))
    author = db.Column(db.String(128))

    level_en = db.relationship('LevelsEn', back_populates='books', uselist=False)
    users_books_history = db.relationship('UsersBooksHistory', back_populates='book', uselist=False)
    books_sentences = db.relationship('BooksSentences', back_populates='book')
