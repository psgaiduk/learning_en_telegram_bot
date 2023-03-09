from db.core import Session
from db.models import users_texts


async def create_texts_users(telegram_id: int, text_id: int):
    """Create item text for user."""
    with Session() as session:
        new_item = users_texts(user_telegram_id=telegram_id, text_id=text_id)
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
