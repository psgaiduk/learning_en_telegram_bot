from pydantic import BaseModel


class MainLanguageDTOModel(BaseModel):
    """Model of main language."""

    id: int
    title: str
    description: str
