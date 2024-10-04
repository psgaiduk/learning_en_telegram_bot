from app import db


class GrammarExercises(db.Model):
    """Model of grammar exercises."""

    __tablename__ = "grammar_exercises"

    grammar_exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_grammar_exercise_id = db.Column(db.ForeignKey("type_grammar_exercises.type_grammar_exercise_id"))
    text = db.Column(db.Text)

    type_grammar_exercise = db.relationship("TypeGrammarExercises", back_populates="grammar_exercises", uselist=False)
    users_grammar_exercises_history = db.relationship("UsersGrammarExercisesHistory", back_populates="grammar_exercise")
