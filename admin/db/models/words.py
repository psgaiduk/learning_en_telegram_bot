from app import db


class Words(db.Model):
    """Model of words."""

    __tablename__ = 'words'

    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_word_id = db.Column(db.ForeignKey('type_words.type_word_id'))
    word = db.Column(db.String(128))
    translation = db.Column(db.JSON)

    type_word = db.relationship('TypeWords', back_populates='words', uselist=False)
    users_words_history = db.relationship('UsersWordsHistory', back_populates='word')
