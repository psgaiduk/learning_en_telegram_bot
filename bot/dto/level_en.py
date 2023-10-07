from pydantic import BaseModel


class LevelEnDTOModel(BaseModel):
    """Model of level en."""

    id: int
    title: str
    description: str
    order: int
