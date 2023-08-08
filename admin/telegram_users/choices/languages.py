from enum import Enum


class Language(Enum):
    """Languages."""

    russian = ('ru', 'Русский язык', 'russian')

    def __init__(self, value, description, language_name) -> None:
        self._value_ = value
        self.description = description
        self.language_name = language_name

    @classmethod
    def choices(cls):
        return [(choice.value, choice.description) for choice in cls]

    @classmethod
    def get_info(cls):
        return [(choice.value, choice.language_name) for choice in cls]
