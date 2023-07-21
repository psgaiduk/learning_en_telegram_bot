from enum import Enum


class Levels(Enum):
    """Levels of the english."""

    A1 = 0, 'A1 - Beginner'
    A2 = 1, 'A2 - Pre-Intermediate'
    B1 = 2, 'B1 - Intermediate'
    B2 = 3, 'B2 - Upper-Intermediate'

    @classmethod
    def get_level_name(cls, level: int) -> str:
        """Get level."""
        if level == 0:
            return cls.A1.value[1]
        elif level == 1:
            return cls.A2.value[1]
        elif level == 2:
            return cls.B1.value[1]
        elif level == 3:
            return cls.B2.value[1]
        else:
            raise ValueError('Level not found.')
