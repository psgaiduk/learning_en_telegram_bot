from pydantic import BaseModel


class CreateReferralUserDTO(BaseModel):
    """Create referral user DTO."""

    telegram_user_id: int
    friend_telegram_id: int
