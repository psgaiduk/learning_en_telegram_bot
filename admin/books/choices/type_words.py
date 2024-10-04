from app.choices import AdminChoiceEnum


class TypeWord(AdminChoiceEnum):
    """Type of words."""

    word = ("word", "Word")
    phrase_verb = ("phrase_verb", "Phrase verb")
    idiomatic_expression = ("idiomatic_expression", "Idiomatic expression")
