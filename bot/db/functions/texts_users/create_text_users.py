from datetime import datetime

from db.core import Session
from db.models import UsersText, Users


async def create_texts_users(user: Users, text_id: int):
    """Create item text for user."""
    with Session() as session:
        new_item = UsersText(
            user_telegram_id=user.telegram_id,
            text_id=text_id,
            language=f'{user.main_language}{user.learn_language}',
            date=int(datetime.utcnow().replace(hour=0, minute=0, second=0).timestamp()),
        )
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
