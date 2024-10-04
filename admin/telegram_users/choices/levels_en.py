from app.choices import AdminChoiceEnum


class LevelEn(AdminChoiceEnum):
    """Levels of English."""

    A1 = ("A1", "beginner")
    A2 = ("A2", "elementary")
    B1 = ("B1", "pre-intermediate")
    B2 = ("B2", "intermediate")
    C1 = ("C1", "upper-intermediate")
    C2 = ("C2", "advanced")
