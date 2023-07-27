from app import db


class LevelsEn(db.Model):
    """Model of level of english."""

    __tablename__ = 'levels_en'

    level_en_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    order = db.Column(db.Integer)

    users = db.relationship('Users', back_populates='level_en')
    type_grammar_exercises = db.relationship('TypeGrammarExercises', back_populates='level_en')
    books = db.relationship('Books', back_populates='level_en')
