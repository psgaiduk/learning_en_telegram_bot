from pydantic import BaseModel


class ReferralUserModelDTO(BaseModel):
    """Referral user model DTO."""

    telegram_id: int
    friends: list[int]
