from pydantic import BaseModel


class MainLanguageDTO(BaseModel):
    """Main language DTO."""

    id: int
    title: str
    description: str
