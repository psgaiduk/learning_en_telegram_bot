from app import db


class BooksSentences(db.Model):
    """Model of books sentences."""

    __tablename__ = 'books_sentences'

    sentence_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    book_id = db.Column(db.ForeignKey('books.book_id'))
    order = db.Column(db.Integer)
    text = db.Column(db.JSON)
    translation = db.Column(db.JSON)
    words = db.Column(db.JSON)

    book = db.relationship('Books', back_populates='books_sentences', uselist=False)
    users_books_sentences_history = db.relationship('UsersBooksSentencesHistory', back_populates='sentence')
