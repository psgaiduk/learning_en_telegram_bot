from pydantic import BaseModel


class UserStatsModelDTO(BaseModel):
    """User's stats DTO."""

    count_of_words: int
    count_of_new_words: int
    time_to_next_word: int
