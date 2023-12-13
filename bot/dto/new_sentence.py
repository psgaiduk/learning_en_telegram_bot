from typing import Optional

from pydantic import BaseModel

from .words import WordDTOModel


class NewSentenceDTOModel(BaseModel):
    """Model of new sentence."""

    history_sentence_id: int
    sentence_id: int
    order: int
    book_id: int
    text: str
    text_with_words: str
    translation: Optional[dict[str, str]]
    words: Optional[list[WordDTOModel]]
