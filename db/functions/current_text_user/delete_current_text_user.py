from db.core import Session
from db.models import CurrentUserText


async def delete_current_text_user(telegram_id: int):
    """Delete item current text user for user."""
    with Session() as session:
        session.query(
            CurrentUserText
        ).filter(
            CurrentUserText.telegram_id == telegram_id,
        ).delete()
        session.commit()
