from pydantic import BaseModel


class WordsModelDTO(BaseModel):
    """Words DTO."""

    word_id: int
    type_word_id: int
    word: str
    translation: dict
