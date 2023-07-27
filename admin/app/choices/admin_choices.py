from enum import Enum


class AdminChoiceEnum(Enum):
    """Base class for all choices for admin."""

    def __init__(self, value, description):
        self._value_ = value
        self.description = description

    @classmethod
    def choices(cls):
        return [(choice.value, choice.description) for choice in cls]
