from pydantic import BaseModel


class LevelsEnModelDTO(BaseModel):
    """DTO of level of english."""

    id: int
    title: str
    description: str
    order: int
