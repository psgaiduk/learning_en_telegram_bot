from pydantic import BaseModel


class HeroLevelDTOModel(BaseModel):
    """Model of hero level."""

    id: int
    title: str
    need_experience: int
    count_sentences: int
    count_games: int
    order: int
