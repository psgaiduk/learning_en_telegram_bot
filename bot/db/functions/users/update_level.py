from db.core import Session
from db.models import Users


async def update_user_level(telegram_id: int, level: int):
    """Update user level."""
    with Session() as session:
        user = session.query(
            Users
        ).filter(
            Users.telegram_id == telegram_id,
        ).first()
        user.level = level
        session.commit()
