from pydantic import BaseModel


class HeroLevelsModelDTO(BaseModel):
    """DTO of hero levels."""

    id: int
    title: str
    need_experience: int
    count_sentences: int
    count_games: int
    order: int
