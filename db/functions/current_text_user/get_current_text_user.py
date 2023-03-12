from db.core import Session
from db.models import CurrentUserText


async def get_current_text_for_user(telegram_id: int) -> CurrentUserText:
    """Function for get current text for user."""
    with Session() as session:
        current_text = session.query(CurrentUserText).filter(
            CurrentUserText.telegram_id == telegram_id,
        )
        return current_text.first()
