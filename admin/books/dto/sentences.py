from pydantic import BaseModel


class SentenceDTO(BaseModel):
    """Sentence DTO."""

    text: str
    index: int
    idiomatic_expression: list = []
    phrase_verb: list = []
    words: list = []
