from pydantic import BaseModel


class WordFromSentenceDTO(BaseModel):
    """
    DTO for word from sentence from gpt.
    """

    word: str
    translate: str
    part_of_speech: str
    transcription: str
