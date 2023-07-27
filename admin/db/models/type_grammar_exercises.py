from app import db


class TypeGrammarExercises(db.Model):
    """Model of type of grammar exercises."""

    __tablename__ = 'type_grammar_exercises'

    type_grammar_exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    level_en_id = db.Column(db.ForeignKey('levels_en.level_en_id'))
    correct_scores = db.Column(db.Integer)
    incorrect_scores = db.Column(db.Integer)

    grammar_exercises = db.relationship('GrammarExercises', back_populates='type_grammar_exercise')
    level_en = db.relationship('LevelsEn', back_populates='type_grammar_exercises', uselist=False)
