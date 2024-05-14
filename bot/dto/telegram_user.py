from typing import Optional

from pydantic import BaseModel

from .hero_level import HeroLevelDTOModel
from .level_en import LevelEnDTOModel
from .main_language import MainLanguageDTOModel
from .new_sentence import NewSentenceDTOModel
from .words import WordDTOModel


class TelegramUserDTOModel(BaseModel):
    """Model of telegram user."""

    telegram_id: int
    user_name: str
    experience: int
    previous_stage: Optional[str]
    stage: str

    main_language: Optional[MainLanguageDTOModel]
    level_en: Optional[LevelEnDTOModel]
    hero_level: Optional[HeroLevelDTOModel]

    new_sentence: Optional[NewSentenceDTOModel]
    learn_words: Optional[list[WordDTOModel]] = []
