from enum import Enum


class EnglishLevels(Enum):
    """English levels."""

    A1 = ('beginner', 1)
    A2 = ('elementary', 2)
    B1 = ('pre-intermediate', 3)
    B2 = ('intermediate', 4)
    C1 = ('upper-intermediate', 5)
    C2 = ('advanced', 6)

    def __new__(cls, description, order):
        obj = object.__new__(cls)
        obj._value_ = description
        obj._order = order
        return obj

    @property
    def level_order(self):
        return self._order
