from app import db


class TypeWords(db.Model):
    """Model of type of words."""

    __tablename__ = 'type_words'

    type_word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))

    words = db.relationship('Words', back_populates='type_word')
